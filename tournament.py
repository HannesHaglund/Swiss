import random
import math
import itertools
from os import linesep
from player import Player
from match_log import MatchLog



class Matchup:
    def __init__(self, player_a, player_b, cost):
        self.player_a = player_a
        self.player_b = player_b
        self.cost = cost

    def is_bye(self):
        return player_b is None


class Matchups:
    def __init__(self):
        self.pairs = []
        self.bye_player = None

    def string(self):
        rslt = ""
        for matchup in self.pairs:
            rslt += (matchup.player_a.name() + " VS. " + \
                     matchup.player_b.name() + linesep)
        if self.bye_player is not None:
            rslt += (self.bye_player.name() + " gets a bye." + linesep)
        return rslt.rstrip() # Remove last endline

    def players_are_matched(self, pa, pb):
        for m in self.pairs:
            if (m.player_a == pa and m.player_b == pb or \
                m.player_a == pb and m.player_b == pa):
                return True
        return False

    def badness(self):
        return sum([m.cost for m in self.pairs])


class Tournament:
    def __init__(self):
        self._match_log = MatchLog()
        self._players = []


    def match_log(self):
        return self._match_log


    def players(self):
        return list(set(self._players + self._match_log.players()))


    def add_player(self, player):
        self._update_players([player])


    def add_result(self, player_a, player_b, wins_a, wins_b):
        self._update_players([player_a, player_b])
        self._match_log.add_result(player_a, player_b, wins_a, wins_b)


    def add_bye(self, player):
        self._update_players([player])
        self._match_log.add_bye(player)


    def add_result_by_names(self, player_a_name, player_b_name, wins_a, wins_b):
        player_a = self._player_name_player(player_a_name)
        player_b = self._player_name_player(player_b_name)
        self._match_log.add_result(player_a, player_b, wins_a, wins_b)


    def add_bye_by_name(self, player_name):
        player = self._player_name_player(player_name)
        self._match_log.add_bye(player)


    def rank_score_pairs(self):
        active_players = [p for p in self._players if p.is_active()]
        score_player_pairs = [(self._match_log.times_match_win(p), p) \
                              for p in active_players]
        pairs_by_name = sorted(score_player_pairs, \
                               key=lambda e: e[1].name())
        pairs_by_win = sorted(pairs_by_name, \
                              key=lambda e: e[0])
        pairs_by_win.reverse() # Best to worst
        return [e for e in pairs_by_win if e[1].is_active()]


    def _player_name_player(self, player_name):
        player = None
        for p in self._players:
            if p.name() == player_name:
                player = p
                break
        if player is None:
            player = Player(player_name)
        self._update_players([player])
        return player


    def _update_players(self, new_players):
        for p in new_players:
            if p not in self._players:
                self._players.append(p)
