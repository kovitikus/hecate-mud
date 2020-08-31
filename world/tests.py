from evennia.utils.test_resources import EvenniaTest
from world import skillsets

class TestSkillsets(EvenniaTest):
    def test_return_rank_bonus(self):
        rank = 3
        difficulty = 'difficult'
        expected_rb = 6.3
        actual_rb = skillsets.return_rank_bonus(rank, difficulty)
        self.assertEqual(expected_rb, actual_rb)

        