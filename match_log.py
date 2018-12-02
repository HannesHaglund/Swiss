from match_result import MatchResult
import networkx as nx
import random

class MatchLog:
    def __init__(self):
        self._entries = []


    def add_result(self, player_a, player_b, wins_a, wins_b):
        self._entries.append(MatchResult(player_a, player_b, wins_a, wins_b))


    def add_bye(self, player):
        self._entries.append(MatchResult(player, None, 0, 0))


    def players(self):
        players_a = [e._player_a \
                     for e in self._entries \
                     if e._player_a is not None];
        players_b = [e._player_b \
                     for e in self._entries \
                     if e._player_b is not None];
        return list(set(players_a + players_b))


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


    def min_active_bye_count(self):
        byes = []
        players = self.active_players()
        for p in players:
            byes.append(self.times_got_bye(p))
        if len(byes) == 0:
            return 0
        else:
            return min(byes)
