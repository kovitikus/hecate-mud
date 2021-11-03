from mock import Mock

from evennia.utils import ansi
from evennia.prototypes.spawner import spawn

from misc.test_resources import HecateTest

class TestInventoryHandler(HecateTest):
    def test_force_item_into_hand(self):
        room1 = self.room1

        char1 = self.char1
        char1.location = room1

        char2 = self.char2
        char2.location = room1

        torch1 = spawn('crudely-made torch')[0]
        torch1.location = room1

        char1_expected_msg = f"You pick up a crudely-made torch({torch1.dbref}) from the ground."
        char2_expected_msg = "Char1 picks up a crudely-made torch from the ground."

        with capture_output(char1, char2) as captured:
            char1.inv.force_item_into_hand(torch1, hand='main')
            self.assertEqual({
                char1: char1_expected_msg,
                char2: char2_expected_msg},
                captured.output())

        self.assertIn(torch1, char1.contents)

        hands = char1.attributes.get('hands')
        self.assertEqual(torch1, hands['main'])
        self.assertEqual(None, hands['off'])

class capture_output(object):
    """
    Context manager used to patch session output sent to objects.
    This can be used to assert expectations against text output to one or
    more receiver objects supplied in the constructor with a single
    assert statement, rather than asserting against multiple mocks in
    sequence.
    Usage:
        with capture_output(obj1, obj2, obj3) as captured:
            # ... Perform calls that generate output.
            self.assertEqual(
                captured.output(),
                {obj1: "Obj1 text", obj2: "Obj2 text", obj3: None}
            )
    """

    def __init__(self, *args):
        """
        Initialize this manager with one or more objects to capture from.
        Args:
            *args: One or more positional args, each of which should be an
                object with an attached session. Output sent to the first
                such session for each object will be captured within the
                scope of this context manager.
        """
        self.obj = args

    def __enter__(self):
        self.patches = {}
        # Upon entry, mock output sessions attached to each object.
        for obj in self.obj:
            sessions = obj.sessions.all() if obj.sessions else None
            if sessions and (session := sessions[0]):
                backup = session.data_out
                mock = Mock()
                session.data_out = mock
                self.patches[obj] = (backup, mock)
        return self

    def __exit__(self, *args):
        for obj, (backup, mock) in self.patches.items():
            sessions = obj.sessions.all() if obj.sessions else None
            if sessions and (session := sessions[0]) and session.data_out == mock:
                session.data_out = backup
        return False

    def output(self, noansi=True):
        """
        Returns captured output.
        Args:
            noansi (bool): True to strip color tags from output. This makes
                assertions more readable if color information does not matter.
        Returns:
            (dict): A dictionary with a key for each object specified when this
                context manager was entered. Each key maps to a string which
                contains all of the output received since the context manager
                was opened, separated by newlines if more than one was present.
                If no output was received for a given object, its value is
                None.
        """
        result = {}
        for obj, (_, mock) in self.patches.items():
            if calls := mock.mock_calls:
                messages = [
                    kwargs.get("text", "") for name, args, kwargs in calls if kwargs
                ]
                messages = [
                    str(text[0]) if isinstance(text, tuple) else str(text)
                    for text in messages
                    if text
                ]
                text = "\n".join(messages)
                text = ansi.parse_ansi(text, strip_ansi=noansi).strip()
                result[obj] = text
            else:
                result[obj] = None

        if len(result) == 1:
            result = next(iter(result.values()))
        return result
