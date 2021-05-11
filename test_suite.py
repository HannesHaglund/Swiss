from player import Player
from match_log import MatchLog
import unittest
import matchup_strategies.min_cost


class TestMatchupPossibilities(unittest.TestCase):

    def setUp(self):
        self.match_log = MatchLog()
        self.players = [Player("player_" + str(i)) for i in range(32)]


    def test_6_players_have_1_possible_matchups(self):
        for i in range(6):
            self.match_log.add_player(self.players[i])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.match_log), 1)


    def test_7_players_have_1_possible_matchups(self):
        for i in range(7):
            self.match_log.add_player(self.players[i])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.match_log), 1)


    def test_players_face_closest_player_in_list(self):
        for i in range(6):
            self.match_log.add_player(self.players[i])
        matchups = matchup_strategies.min_cost.pairings(self.match_log)
        self.assertTrue(matchups.players_are_matched(self.players[0], self.players[1]))
        self.assertTrue(matchups.players_are_matched(self.players[2], self.players[3]))
        self.assertTrue(matchups.players_are_matched(self.players[4], self.players[5]))

    def test_players_face_closest_player_in_list_after_one_round(self):
        for i in range(8):
            self.match_log.add_player(self.players[i])
        matchups = matchup_strategies.min_cost.pairings(self.match_log)
        for matchup in matchups.pairs:
            self.match_log.add_result(matchup.player_a, matchup.player_b, 1, 0)
        self.assertEqual(self.match_log.times_match_win(self.players[0]), 1)
        self.assertEqual(self.match_log.times_match_win(self.players[1]), 0)
        self.assertEqual(self.match_log.times_match_win(self.players[2]), 1)
        self.assertEqual(self.match_log.times_match_win(self.players[3]), 0)
        self.assertEqual(self.match_log.times_match_win(self.players[4]), 1)
        self.assertEqual(self.match_log.times_match_win(self.players[5]), 0)
        self.assertEqual(self.match_log.times_match_win(self.players[6]), 1)
        self.assertEqual(self.match_log.times_match_win(self.players[7]), 0)
        matchups = matchup_strategies.min_cost.pairings(self.match_log)
        self.assertTrue(matchups.players_are_matched(self.players[0], self.players[2]))
        self.assertTrue(matchups.players_are_matched(self.players[4], self.players[6]))
        self.assertTrue(matchups.players_are_matched(self.players[1], self.players[3]))
        self.assertTrue(matchups.players_are_matched(self.players[5], self.players[7]))

    def test_4_players_two_rounds(self):
        for i in range(4):
            self.match_log.add_player(self.players[i])
        # First round
        matchups = matchup_strategies.min_cost.pairings(self.match_log)
        for matchup in matchups.pairs:
            self.match_log.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.match_log.ranking()
        self.assertEqual(self.match_log.player_score(ranking[0]), 1)
        self.assertEqual(self.match_log.player_score(ranking[1]), 1)
        self.assertEqual(self.match_log.player_score(ranking[2]), 0)
        self.assertEqual(self.match_log.player_score(ranking[3]), 0)
        # Second round
        matchups = matchup_strategies.min_cost.pairings(self.match_log)
        for matchup in matchups.pairs:
            self.match_log.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.match_log.ranking()
        self.assertEqual(self.match_log.player_score(ranking[0]), 2)
        self.assertEqual(self.match_log.player_score(ranking[1]), 1)
        self.assertEqual(self.match_log.player_score(ranking[2]), 1)
        self.assertEqual(self.match_log.player_score(ranking[3]), 0)


    def test_8_players_three_rounds(self):
        for i in range(8):
            self.match_log.add_player(self.players[i])
        # First round
        matchups = matchup_strategies.min_cost.pairings(self.match_log)
        for matchup in matchups.pairs:
            self.match_log.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.match_log.ranking()
        self.assertEqual(self.match_log.player_score(ranking[0]), 1)
        self.assertEqual(self.match_log.player_score(ranking[1]), 1)
        self.assertEqual(self.match_log.player_score(ranking[2]), 1)
        self.assertEqual(self.match_log.player_score(ranking[3]), 1)
        self.assertEqual(self.match_log.player_score(ranking[4]), 0)
        self.assertEqual(self.match_log.player_score(ranking[5]), 0)
        self.assertEqual(self.match_log.player_score(ranking[6]), 0)
        self.assertEqual(self.match_log.player_score(ranking[7]), 0)
        # Second round
        matchups = matchup_strategies.min_cost.pairings(self.match_log)
        for matchup in matchups.pairs:
            self.match_log.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.match_log.ranking()
        self.assertEqual(self.match_log.player_score(ranking[0]), 2)
        self.assertEqual(self.match_log.player_score(ranking[1]), 2)
        self.assertEqual(self.match_log.player_score(ranking[2]), 1)
        self.assertEqual(self.match_log.player_score(ranking[3]), 1)
        self.assertEqual(self.match_log.player_score(ranking[4]), 1)
        self.assertEqual(self.match_log.player_score(ranking[5]), 1)
        self.assertEqual(self.match_log.player_score(ranking[6]), 0)
        self.assertEqual(self.match_log.player_score(ranking[7]), 0)
        # Third round
        matchups = matchup_strategies.min_cost.pairings(self.match_log)
        for matchup in matchups.pairs:
            self.match_log.add_result(matchup.player_a, matchup.player_b, 1, 0)
        ranking = self.match_log.ranking()
        self.assertEqual(self.match_log.player_score(ranking[0]), 3)
        self.assertEqual(self.match_log.player_score(ranking[1]), 2)
        self.assertEqual(self.match_log.player_score(ranking[2]), 2)
        self.assertEqual(self.match_log.player_score(ranking[3]), 2)
        self.assertEqual(self.match_log.player_score(ranking[4]), 1)
        self.assertEqual(self.match_log.player_score(ranking[5]), 1)
        self.assertEqual(self.match_log.player_score(ranking[6]), 1)
        self.assertEqual(self.match_log.player_score(ranking[7]), 0)


    def test_ranking(self):
        self.match_log.add_player(self.players[0])
        self.match_log.add_player(self.players[1])
        self.assertEqual(self.match_log.ranking(), [self.players[0], self.players[1]])
        self.match_log.add_result(self.players[1], self.players[0], 1, 0)
        self.assertEqual(self.match_log.ranking(), [self.players[1], self.players[0]])


    def test_player_score(self):
        self.match_log.add_player(self.players[0])
        self.match_log.add_player(self.players[1])
        self.assertEqual(self.match_log.player_score(self.players[0]), 0)
        self.assertEqual(self.match_log.player_score(self.players[1]), 0)
        self.match_log.add_result(self.players[1], self.players[0], 1, 0)
        self.assertEqual(self.match_log.player_score(self.players[0]), 0)
        self.assertEqual(self.match_log.player_score(self.players[1]), 1)


    def test_no_players(self):
        m = matchup_strategies.min_cost.pairings(self.match_log)
        self.assertEqual(m.pairs, [])
        self.assertIsNone(m.bye_player, None)
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.match_log), 1)


    def test_one_player(self):
        self.match_log.add_player(self.players[0])
        m = matchup_strategies.min_cost.pairings(self.match_log)
        self.assertEqual(m.pairs, [])
        self.assertEqual(m.bye_player, self.players[0])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.match_log), 1)


    def test_two_players(self):
        self.match_log.add_player(self.players[0])
        self.match_log.add_player(self.players[1])
        m = matchup_strategies.min_cost.pairings(self.match_log)
        self.assertTrue(m.players_are_matched(self.players[0], self.players[1]))
        self.assertEqual(len(m.pairs), 1)
        self.assertIsNone(m.bye_player, None)
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.match_log), 1)


    def test_player_added_twice_should_be_the_same_as_added_once(self):
        self.match_log.add_player(self.players[0])
        self.match_log.add_player(self.players[0])
        m = matchup_strategies.min_cost.pairings(self.match_log)
        self.assertEqual(m.pairs, [])
        self.assertEqual(m.bye_player, self.players[0])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.match_log), 1)


    def test_three_players_worst_performer_gets_bye(self):
        self.match_log.add_player(self.players[0])
        self.match_log.add_player(self.players[1])
        self.match_log.add_player(self.players[2])
        self.match_log.add_result(self.players[0], self.players[1], 1, 0)
        self.match_log.add_result(self.players[1], self.players[2], 1, 0)
        m = matchup_strategies.min_cost.pairings(self.match_log)
        self.assertTrue(m.players_are_matched(self.players[0], self.players[1]))
        self.assertEqual(len(m.pairs), 1)
        self.assertEqual(m.bye_player, self.players[2])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.match_log), 1)


    def test_byed_player_dont_get_byed_again(self):
        self.match_log.add_player(self.players[0])
        self.match_log.add_player(self.players[1])
        self.match_log.add_player(self.players[2])
        self.match_log.add_result(self.players[0], self.players[1], 1, 0)
        self.match_log.add_result(self.players[0], self.players[2], 1, 0)
        self.match_log.add_bye(self.players[1])
        self.match_log.add_bye(self.players[2])
        m = matchup_strategies.min_cost.pairings(self.match_log)
        self.assertTrue(m.players_are_matched(self.players[1], self.players[2]))
        self.assertEqual(len(m.pairs), 1)
        self.assertEqual(m.bye_player, self.players[0])
        self.assertEqual(matchup_strategies.min_cost.number_of_possible_pairings(self.match_log), 1)

    def test_smoke_pairings_string(self):
        self.match_log.add_player(self.players[0])
        self.match_log.add_player(self.players[1])
        s = matchup_strategies.min_cost.pairings(self.match_log).string()
        vs_s = self.players[0].name() + ' VS. ' + self.players[1].name()
        self.assertEqual(s, vs_s)

if __name__ == "__main__":
    unittest.main()
