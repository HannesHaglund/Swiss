import math
import itertools
import matchup_strategies.min_cost
from random import shuffle
from os import linesep
from player import Player, bye_dummy
from match_log import MatchLog
from ranking import Ranking


class Tournament:
    def __init__(self, matchup_strategy=matchup_strategies.min_cost):
        self._matchup_strategy = matchup_strategy
        self._match_log = MatchLog()
        self._players = []


    def cost_map(self):
        return self._matchup_strategy.cost_map(self)


    def match_log(self):
        return self._match_log


    def players(self):
        return self._players


    def add_player(self, player):
        self._update_players([player])


    def randomize_player_order(self):
        shuffle(self._players)


    def add_result(self, player_a, player_b, wins_a, wins_b):
        self._update_players([player_a, player_b])
        self._match_log.add_result(player_a, player_b, wins_a, wins_b)


    def add_bye(self, player):
        self._update_players([player])
        self._match_log.add_bye(player)


    def add_result_by_names(self, player_a_name, player_b_name, wins_a, wins_b):
        player_a = self.player_name_player(player_a_name)
        player_b = self.player_name_player(player_b_name)
        self._match_log.add_result(player_a, player_b, wins_a, wins_b)


    def add_bye_by_name(self, player_name):
        player = self.player_name_player(player_name)
        self._match_log.add_bye(player)


    def pairings(self):
        return self._matchup_strategy.pairings(self)


    def number_of_possible_pairings(self):
        return self._matchup_strategy.number_of_possible_pairings(self)


    def ranking(self):
        r = Ranking()
        active_players = [p for p in self._players if p.is_active()]
        for p in active_players:
            r.add_entry(p, self._match_log.times_match_win(p))
        return r


    def player_number_of_player(self, player):
        match_log_players = self._match_log.players()
        for p in match_log_players:
            assert(p in self._players)
        for i,p in enumerate(self._players):
            if p == player:
                return i
        if player == bye_dummy():
            return len(self._players)
        raise Exception("Player (named " + player.name() + ") not among tournament players")


    def player_name_player(self, player_name):
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
