from tournament import Tournament
from player import Player
import unittest

class TestMatchupPossibilities(unittest.TestCase):

    def setUp(self):
        self.tournament = Tournament()
        self.players = [Player(str(i)) for i in range(32)]

    def test_no_players(self):
        m = self.tournament.round_matchups()
        self.assertEqual(m.pairs, [])
        self.assertIsNone(m.bye_player, None)

    def test_one_player(self):
        self.tournament.add_player(self.players[0])
        m = self.tournament.round_matchups()
        self.assertEqual(m.pairs, [])
        self.assertEqual(m.bye_player, self.players[0])

    def test_two_players(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[1])
        m = self.tournament.round_matchups()
        self.assertTrue(m.players_are_matched(self.players[0], self.players[1]))
        self.assertEquals(len(m.pairs), 1)
        self.assertIsNone(m.bye_player, None)

    def test_player_added_twice_should_be_the_same_as_added_once(self):
        self.tournament.add_player(self.players[0])
        self.tournament.add_player(self.players[0])
        m = self.tournament.round_matchups()
        self.assertEqual(m.pairs, [])
        self.assertEqual(m.bye_player, self.players[0])


if __name__ == "__main__":
    unittest.main()
