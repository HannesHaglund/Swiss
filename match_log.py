from match_result import MatchResult
import player
import networkx as nx
import random

class MatchLog:
    def __init__(self):
        self._entries = []
        self._explicit_players = []


    def add_player(self, player_name):
        if player_name not in self._explicit_players:
            self._explicit_players.append(player_name)


    def add_result(self, player_a, player_b, wins_a, wins_b):
        self.add_player(player_a)
        self.add_player(player_b)
        self._entries.append(MatchResult(player_a, player_b, wins_a, wins_b))


    def add_bye(self, player):
        self._entries.append(MatchResult(player, None, 0, 0))


    def players(self):
        # Add dummy if we're an odd number of players
        if len(self._explicit_players) % 2 == 0:
            return self._explicit_players
        else:
            return self._explicit_players + [player.bye_dummy()]


    def active_players(self):
        return [p for p in self.players() if p.is_active()]


    def times_matched(self, player_a, player_b):
        rslt = 0
        for entry in self._entries:
            if entry.has_players(player_a, player_b):
                rslt += 1
        return rslt


    def times_got_bye(self, player):
        rslt = 0
        for entry in self._entries:
            if entry.is_bye() and entry.winner() == player:
                rslt += 1
        return rslt


    def times_match_win(self, player):
        rslt = 0
        for entry in self._entries:
            winner = entry.winner()
            if winner == player:
                rslt += 1
        return rslt


    def player_score(self, player):
        rslt = 0
        for entry in self._entries:
            if entry.player_a() == player:
                rslt += entry.player_a_wins()
            if entry.player_b() == player:
                rslt += entry.player_b_wins()
        return rslt


    def min_active_bye_count(self):
        byes = []
        players = self.active_players()
        for p in players:
            byes.append(self.times_got_bye(p))
        if len(byes) == 0:
            return 0
        else:
            return min(byes)


    def ranking(self):
        return sorted(self.players(), key=lambda e: self.player_score(e), reverse=True)
