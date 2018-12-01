from tournament import Tournament
from player import Player
import unittest
import matchup_strategies.min_cost


class TestMatchupPossibilities(unittest.TestCase):

    def setUp(self):
        self.tournament = Tournament()
        self.players = [Player(str(i)) for i in range(32)]


    def test_6_players_have_15_possible_matchups(self):
        for i in range(6):
            self.tournament.add_player(self.players[i])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 15)


    def test_7_players_have_105_possible_matchups(self):
        for i in range(7):
            self.tournament.add_player(self.players[i])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 105)


    def test_6_players_result_removes_3_matchups(self):
        for i in range(6):
            self.tournament.add_player(self.players[i])
        self.tournament.add_result(self.players[0], self.players[1], 1, 0)
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 15 - 3)


    def test_4_players_two_rounds(self):
        for i in range(4):
            self.tournament.add_player(self.players[i])
        # First round
        matchups = matchup_strategies.min_cost.pairings(self.tournament)
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.rank_score_pairs()
        self.assertEqual(ranking[0][0], 1)
        self.assertEqual(ranking[1][0], 1)
        self.assertEqual(ranking[2][0], 0)
        self.assertEqual(ranking[3][0], 0)
        # Second round
        matchups = matchup_strategies.min_cost.pairings(self.tournament)
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.rank_score_pairs()
        self.assertEqual(ranking[0][0], 2)
        self.assertEqual(ranking[1][0], 1)
        self.assertEqual(ranking[2][0], 1)
        self.assertEqual(ranking[3][0], 0)


    def test_8_players_three_rounds(self):
        for i in range(8):
            self.tournament.add_player(self.players[i])
        # First round
        matchups = matchup_strategies.min_cost.pairings(self.tournament)
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.rank_score_pairs()
        self.assertEqual(ranking[0][0], 1)
        self.assertEqual(ranking[1][0], 1)
        self.assertEqual(ranking[2][0], 1)
        self.assertEqual(ranking[3][0], 1)
        self.assertEqual(ranking[4][0], 0)
        self.assertEqual(ranking[5][0], 0)
        self.assertEqual(ranking[6][0], 0)
        self.assertEqual(ranking[7][0], 0)
        # Second round
        matchups = matchup_strategies.min_cost.pairings(self.tournament)
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.rank_score_pairs()
        self.assertEqual(ranking[0][0], 2)
        self.assertEqual(ranking[1][0], 2)
        self.assertEqual(ranking[2][0], 1)
        self.assertEqual(ranking[3][0], 1)
        self.assertEqual(ranking[4][0], 1)
        self.assertEqual(ranking[5][0], 1)
        self.assertEqual(ranking[6][0], 0)
        self.assertEqual(ranking[7][0], 0)
        # Third round
        matchups = matchup_strategies.min_cost.pairings(self.tournament)
        for matchup in matchups.pairs:
            self.tournament.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.tournament.rank_score_pairs()
        self.assertEqual(ranking[0][0], 3)
        self.assertEqual(ranking[1][0], 2)
        self.assertEqual(ranking[2][0], 2)
        self.assertEqual(ranking[3][0], 2)
        self.assertEqual(ranking[4][0], 1)
        self.assertEqual(ranking[5][0], 1)
        self.assertEqual(ranking[6][0], 1)
        self.assertEqual(ranking[7][0], 0)


    def test_no_players(self):
        m = matchup_strategies.min_cost.pairings(self.tournament)
        self.assertEqual(m.pairs, [])
        self.assertIsNone(m.bye_player, None)
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 1)


    def test_one_player(self):
        self.tournament.add_player(self.players[0])
        m = matchup_strategies.min_cost.pairings(self.tournament)
        self.assertEqual(m.pairs, [])
        self.assertEqual(m.bye_player, self.players[0])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 1)


    def test_two_players(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[1])
        m = matchup_strategies.min_cost.pairings(self.tournament)
        self.assertTrue(m.players_are_matched(self.players[0], self.players[1]))
        self.assertEqual(len(m.pairs), 1)
        self.assertIsNone(m.bye_player, None)
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 1)


    def test_player_added_twice_should_be_the_same_as_added_once(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[0])
        m = matchup_strategies.min_cost.pairings(self.tournament)
        self.assertEqual(m.pairs, [])
        self.assertEqual(m.bye_player, self.players[0])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 1)


    def test_three_players_worst_performer_gets_bye(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[1])
        self.tournament.add_player(self.players[2])
        self.tournament.add_result(self.players[0], self.players[1], 1, 0)
        self.tournament.add_result(self.players[1], self.players[2], 1, 0)
        m = matchup_strategies.min_cost.pairings(self.tournament)
        self.assertTrue(m.players_are_matched(self.players[0], self.players[1]))
        self.assertEqual(len(m.pairs), 1)
        self.assertEqual(m.bye_player, self.players[2])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 1)


    def test_byed_player_dont_get_byed_again(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[1])
        self.tournament.add_player(self.players[2])
        self.tournament.add_result(self.players[0], self.players[1], 1, 0)
        self.tournament.add_result(self.players[0], self.players[2], 1, 0)
        self.tournament.add_bye(self.players[1])
        self.tournament.add_bye(self.players[2])
        m = matchup_strategies.min_cost.pairings(self.tournament)
        self.assertTrue(m.players_are_matched(self.players[1], self.players[2]))
        self.assertEqual(len(m.pairs), 1)
        self.assertEqual(m.bye_player, self.players[0])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 1)


    def test_first_round_any_player_can_be_randomly_byed(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[1])
        self.tournament.add_player(self.players[2])
        max_attempts = 8192
        byed_players = set()
        for i in range(max_attempts):
            m = matchup_strategies.min_cost.pairings(self.tournament)
            self.assertEqual(len(m.pairs), 1)
            self.assertIsNotNone(m.bye_player)
            byed_players.add(m.bye_player)
            if len(byed_players) == 3:
                break
        self.assertEqual(len(byed_players), 3)
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.tournament), 3)

if __name__ == "__main__":
    unittest.main()
