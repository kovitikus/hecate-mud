from evennia import DefaultObject
from evennia.utils import create
from evennia.utils import logger
from evennia.utils import ansi
from world.generic_str import article

class Object(DefaultObject):
    def get_numbered_name(self, count, looker, **kwargs):
        """
        Return the numbered (singular, plural) forms of this object's key. This is by default called
        by return_appearance and is used for grouping multiple same-named of this object. Note that
        this will be called on *every* member of a group even though the plural name will be only
        shown once. Also the singular display version, such as 'an apple', 'a tree' is determined
        from this method.
        Args:
            count (int): Number of objects of this type
            looker (Object): Onlooker. Not used by default.
        Kwargs:
            key (str): Optional key to pluralize, if given, use this instead of the object's key.
        Returns:
            singular (str): The singular form to display.
            plural (str): The determined plural form of the key, including the count.
        """
        key = kwargs.get("key", self.key)
        key = ansi.ANSIString(key)  # this is needed to allow inflection of colored names
        singular = key
        plural = key
        return singular, plural

    @classmethod
    def create(cls, key, account=None, **kwargs):
        """
        Creates a basic object with default parameters, unless otherwise
        specified or extended.
        Provides a friendlier interface to the utils.create_object() function.
        Args:
            key (str): Name of the new object.
            account (Account): Account to attribute this object to.
        Kwargs:
            description (str): Brief description for this object.
            ip (str): IP address of creator (for object auditing).
        Returns:
            object (Object): A newly created object of the given typeclass.
            errors (list): A list of errors in string form, if any.
        """
        errors = []
        obj = None

        # Get IP address of creator, if available
        ip = kwargs.pop('ip', '')

        # If no typeclass supplied, use this class
        kwargs['typeclass'] = kwargs.pop('typeclass', cls)

        # Set the supplied key as the name of the intended object
        art = article(key)
        key = f"{art} {key}"
        kwargs['key'] = key

        # Get a supplied description, if any
        description = kwargs.pop('description', '')

        # Create a sane lockstring if one wasn't supplied
        lockstring = kwargs.get('locks')
        if account and not lockstring:
            lockstring = cls.lockstring.format(account_id=account.id)
            kwargs['locks'] = lockstring

        # Create object
        try:
            obj = create.create_object(**kwargs)

            # Record creator id and creation IP
            if ip: obj.db.creator_ip = ip
            if account: obj.db.creator_id = account.id

            # Set description if there is none, or update it if provided
            if description or not obj.db.desc:
                desc = description if description else "You see nothing special."
                obj.db.desc = desc

        except Exception as e:
            errors.append("An error occurred while creating this '%s' object." % key)
            logger.log_err(e)

        return obj, errors

    pass

class ObjHands(Object):
    def return_appearance(self, looker, **kwargs):
        looker.msg(f"You see nothing spectacular about your {self.key}.")

class Staves(Object):
    def at_object_creation(self):
        self.attributes.add('wieldable', 2)

class OffHand(Object):
    def at_object_creation(self):
        self.attributes.add('wieldable', 1)
class Shields(OffHand):
    pass
