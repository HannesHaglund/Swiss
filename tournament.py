import networkx as nx
import random
import operator
from player import Player
from match_log import MatchLog


class Matchup:
    player_a = None
    player_b = None
    cost = 0


    def is_bye(self):
        return player_b is None


    def __init__(self, player_a, player_b, cost):
        self.player_a = player_a
        self.player_b = player_b
        self.cost = cost


class Matchups:
    pairs = []
    bye_player = None


class Tournament:
    _match_log = MatchLog()
    _players = []

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


    def round_matchups(self):
        bye = self._match_log.best_bye_candidate()
        graph = self._match_log.matchup_graph(bye)
        mate = nx.max_weight_matching(graph, maxcardinality=True)

        # Extract pairs
        matched_players = []
        pairs = []
        for k, v in mate:
            matched_players.append(k)
            if (k, v) not in pairs:
                pairs.append((k, v))

        # Sort pairs by wins
        wins = self._match_log.players_match_wins()
        for i, pair in enumerate(pairs):
            if wins[pair[0]] < wins[pair[1]]:
                pairs[i] = (pair[1], pair[0])

        # Format as matchups
        matchups = Matchups()
        for e in pairs:
            cost = self._match_log.matchup_cost(e[0], e[1])
            matchups.pairs.append(Matchup(e[0], e[1], cost))
        matchups.bye_player = bye

        return matchups


    def print_round_matchups(self):
        matchups = self.round_matchups()
        for matchup in matchups.pairs:
            print(matchup.player_a.name() \
                  + " VS. " \
                  + matchup.player_b.name())
        if matchups.bye_player is not None:
            print(matchups.bye_player.name(), \
                  "gets a bye.")


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
