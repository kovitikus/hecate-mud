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

    def test_ap_req_list(self):
        rank = 6
        self.assertEqual(skillsets.desired_rank_ap_req[rank-2], 30)

    def test_generate_ap(self):
        rank = 6
        ap_required_to_lvl = skillsets.generate_ap(rank)
        self.assertEqual(ap_required_to_lvl, 30)

    def test_return_rank_score(self):
        rank = 3
        difficulty = 'difficult'
        expected_rs = 6.3
        actual_rs = skillsets.return_rank_score(rank, difficulty)
        self.assertEqual(expected_rs, actual_rs)

    def test_return_defense_skills(self):
        item_skillset = 'staves'
        high_rs, mid_rs, low_rs = skillsets.return_defense_skills(self.char1, item_skillset, rs_only=True)
        high_skill, mid_skill, low_skill = skillsets.return_defense_skills(self.char1, item_skillset, skills_only=True)
        self.assertEqual(high_rs, 10.2)
        self.assertEqual(high_skill, 'stave overhead block')
        self.assertEqual(mid_rs, 6)
        self.assertEqual(mid_skill, 'stave mid block')
        self.assertEqual(low_rs, 7.6499999999999995)
        self.assertEqual(low_skill, 'stave low block')

    def test_defense_layer_calc(self):
        high_def_rs, mid_def_rs, low_def_rs = skillsets.defense_layer_calc(self.char1, rs_only=True)
        high_skills, mid_skills, low_skills = skillsets.defense_layer_calc(self.char1, skills_only=True)
        self.assertEqual(high_def_rs, 10.2)
        self.assertEqual(high_skills, ['stave overhead block', None, None])
        self.assertEqual(mid_def_rs, 6)
        self.assertEqual(mid_skills, ['stave mid block', None, None])
        self.assertEqual(low_def_rs, 7.6499999999999995)
        self.assertEqual(low_skills, ['stave low block', None, None])