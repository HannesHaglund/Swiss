import random
import math
import itertools
from os import linesep
from player import Player
from match_log import MatchLog


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
        return pairs_by_win


    def ranking_string(self):
        rslt = ""
        rank = self.rank_score_pairs()
        max_name_length = max([len(e[1].name()) for e in rank])
        max_numerals = len(str(len(rank)))
        for i,e in enumerate(rank):
            layout = "#{:<" + str(max_numerals) + "}: {: <" + str(max_name_length) + "} {}"
            cols = [str(i), e[1].name(), "("+str(e[0])+" wins)"]
            rslt += layout.format(*cols)
            rslt += linesep
        return rslt


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
