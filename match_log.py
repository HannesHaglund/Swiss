import networkx as nx
import random

class MatchResult:
    def __init__(self, player_a, player_b, wins_a, wins_b):
        self._player_a = player_a
        self._player_b = player_b
        self._player_a_wins = wins_a
        self._player_b_wins = wins_b


    def has_players(self, player_a, player_b):
        return ((self._player_a == player_a and self._player_b == player_b) \
            or (self._player_a == player_b and self._player_b == player_a))


    def is_bye(self):
        return (self._player_a is None or \
                self._player_b is None)


    def winner(self):
        if (self._player_a is not None and \
            self._player_b is None):
            return self._player_a
        if (self._player_b is not None and \
            self._player_a is None):
            return self._player_b
        if self._player_a_wins > self._player_b_wins:
            return self._player_a
        if self._player_b_wins > self._player_a_wins:
            return self._player_b
        return None


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
