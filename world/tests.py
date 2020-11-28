from evennia.utils.test_resources import EvenniaTest
from evennia.utils import create
from world import skillsets
from world import general_mechanics as gen_mec

# Assertions are given arguments in the form of (actual_result, expected_result)

# class TestEquipmentHandler(EvenniaTest):
#     def setUp(self):
#         super().setUp()
#         self.basic_bag = create.create_object(typeclass='typeclasses.objects.InventoryContainer', key='Basic Bag')
#         self.char_test = create.create_object(typeclass='typeclasses.characters.Character', key='Test Char')
    
#     def tearDown(self):
#         super().tearDown()
#         self.basic_bag.delete()
#         self.char_test.delete()

#     def test_equipment_generation(self):
#         equip_dic = {'head': None, 'neck': None, 'shoulder': None, 'chest': None, 'arms': None, 'hands': None,
#                         'fingers': None, 'waist': None, 'thighs': None, 'calves': None, 'feet': None, 'bag': self.basic_bag}
#         actual_dic = dict(self.char_test.attributes.get('equipment'))
#         self.assertDictEqual(equip_dic, actual_dic)


class TestGeneralMechanics(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char_test = create.create_object(typeclass='typeclasses.characters.Character', key='Test Char')

    def tearDown(self):
        super().tearDown()
        self.char_test.delete()

    def test_add_coin(self):
        gen_mec.add_coin(self.char_test, plat=222, gold=999, silver=2222, copper=222)
        coin_dic = self.char_test.attributes.get('coin')
        plat_dic = coin_dic['plat']
        gold_dic = coin_dic['gold']
        silver_dic = coin_dic['silver']
        copper_dic = coin_dic['copper']
        self.assertEqual(223, plat_dic)
        self.assertEqual(1, gold_dic)
        self.assertEqual(222, silver_dic)
        self.assertEqual(222, copper_dic)

# class TestSkillsets(EvenniaTest):
#     def setUp(self):
#         super().setUp()
#         self.stave = create.create_object(
#             'typeclasses.objects.Staves', key="stave", location=self.room1, home=self.room1
#         )
#         self.char1.attributes.add('staves', {'overhead block': 4, 'mid block': 2, 'low block': 3})
#         self.char1.attributes.add('wielding', {'left': None, 'right': None, 'both': self.stave})
#     def tearDown(self):
#         super().tearDown()
#         self.stave.delete()

    # def test_return_rank_score(self):
    #     rank = 3
    #     difficulty = 'difficult'
    #     expected_rs = 6.3
    #     actual_rs = skillsets.return_rank_score(rank, difficulty)
    #     self.assertEqual(expected_rs, actual_rs)

    # def test_return_defense_skills(self):
    #     item_skillset = 'staves'
    #     high_rs, mid_rs, low_rs = skillsets.return_defense_skills(self.char1, item_skillset, rs_only=True)
    #     high_skill, mid_skill, low_skill = skillsets.return_defense_skills(self.char1, item_skillset, skills_only=True)
    #     self.assertEqual(high_rs, 10.2)
    #     self.assertEqual(high_skill, 'stave overhead block')
    #     self.assertEqual(mid_rs, 6)
    #     self.assertEqual(mid_skill, 'stave mid block')
    #     self.assertEqual(low_rs, 7.6499999999999995)
    #     self.assertEqual(low_skill, 'stave low block')

    # def test_defense_layer_calc(self):
    #     high_def_rs, mid_def_rs, low_def_rs = skillsets.defense_layer_calc(self.char1, rs_only=True)
    #     high_skills, mid_skills, low_skills = skillsets.defense_layer_calc(self.char1, skills_only=True)
    #     self.assertEqual(high_def_rs, 10.2)
    #     self.assertEqual(high_skills, ['stave overhead block', None, None])
    #     self.assertEqual(mid_def_rs, 6)
    #     self.assertEqual(mid_skills, ['stave mid block', None, None])
    #     self.assertEqual(low_def_rs, 7.6499999999999995)
    #     self.assertEqual(low_skills, ['stave low block', None, None])