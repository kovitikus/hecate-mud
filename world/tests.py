from evennia.utils.test_resources import EvenniaTest
from evennia.utils import create
from world import skillsets

# Assertions are given arguments in the form of (actual_result, expected_result)
class TestSkillsets(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.stave = create.create_object(
            'typeclasses.objects.Staves', key="stave", location=self.room1, home=self.room1
        )
    def tearDown(self):
        super().tearDown()
        self.stave.delete()

    def test_return_rank_bonus(self):
        rank = 3
        difficulty = 'difficult'
        expected_rb = 6.3
        actual_rb = skillsets.return_rank_bonus(rank, difficulty)
        self.assertEqual(expected_rb, actual_rb)

    def test_return_defense_skills(self):
        char = self.char1
        char.attributes.add('staves', {'overhead block': 4, 'mid block': 2, 'low block': 3})
        item_skillset = 'staves'
        high_rb, mid_rb, low_rb = skillsets.return_defense_skills(char, item_skillset, rb_only=True)
        high_skill, mid_skill, low_skill = skillsets.return_defense_skills(char, item_skillset, skills_only=True)
        self.assertEqual(high_rb, 10.2)
        self.assertEqual(high_skill, 'overhead block')
        self.assertEqual(mid_rb, 6)
        self.assertEqual(mid_skill, 'mid block')
        self.assertEqual(low_rb, 7.6499999999999995)
        self.assertEqual(low_skill, 'low block')

    def test_defense_layer_calc(self):
        char = self.char1
        char.attributes.add('staves', {'overhead block': 4, 'mid block': 2, 'low block': 3})
        char.attributes.add('wielding', {'left': None, 'right': None, 'both': self.stave})
        high_def_rb, mid_def_rb, low_def_rb = skillsets.defense_layer_calc(char, rb_only=True)
        high_skills, mid_skills, low_skills = skillsets.defense_layer_calc(char, skills_only=True)
        self.assertEqual(high_def_rb, 10.2)
        self.assertEqual(high_skills, ['overhead block', '', ''])
        self.assertEqual(mid_def_rb, 6)
        self.assertEqual(mid_skills, ['mid block', '', ''])
        self.assertEqual(low_def_rb, 7.6499999999999995)
        self.assertEqual(low_skills, ['low block', '', ''])