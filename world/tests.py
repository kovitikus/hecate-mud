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
        self.char1.attributes.add('staves', {'overhead block': 4, 'mid block': 2, 'low block': 3})
        self.char1.attributes.add('wielding', {'left': None, 'right': None, 'both': self.stave})
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
        item_skillset = 'staves'
        high_rb, mid_rb, low_rb = skillsets.return_defense_skills(self.char1, item_skillset, rb_only=True)
        high_skill, mid_skill, low_skill = skillsets.return_defense_skills(self.char1, item_skillset, skills_only=True)
        self.assertEqual(high_rb, 10.2)
        self.assertEqual(high_skill, 'stave overhead block')
        self.assertEqual(mid_rb, 6)
        self.assertEqual(mid_skill, 'stave mid block')
        self.assertEqual(low_rb, 7.6499999999999995)
        self.assertEqual(low_skill, 'stave low block')

    def test_defense_layer_calc(self):
        high_def_rb, mid_def_rb, low_def_rb = skillsets.defense_layer_calc(self.char1, rb_only=True)
        high_skills, mid_skills, low_skills = skillsets.defense_layer_calc(self.char1, skills_only=True)
        self.assertEqual(high_def_rb, 10.2)
        self.assertEqual(high_skills, ['stave overhead block', None, None])
        self.assertEqual(mid_def_rb, 6)
        self.assertEqual(mid_skills, ['stave mid block', None, None])
        self.assertEqual(low_def_rb, 7.6499999999999995)
        self.assertEqual(low_skills, ['stave low block', None, None])