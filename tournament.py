import networkx as nx
from player import Player

class MatchResult:
    _player_a = None
    _player_b = None
    _player_a_wins = 0
    _player_b_wins = 0

    def has_players(self, player_a, player_b):
        return ((self._player_a == player_a and self._player_b == player_b) \
            or (self._player_a == player_b and self._player_b == player_a))

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

    def __init__(self, player_a, player_b, wins_a, wins_b):
        self._player_a = player_a
        self._player_b = player_b
        self._player_a_wins = wins_a
        self._player_b_wins = wins_b


class Matchup:
    player_a = None
    player_b = None
    cost = 0

    def __init__(self, player_a, player_b, cost):
        self.player_a = player_a
        self.player_b = player_b
        self.cost = cost


class Tournament:
    _match_log = []

    def add_result(self, player_a, player_b, wins_a, wins_b):
        self._match_log.append(MatchResult(player_a, player_b, wins_a, wins_b))

    def add_result_by_names(self, player_a_name, player_b_name, wins_a, wins_b):
        players = self.players()
        player_a = None
        player_b = None
        for p in players:
            if p.name() == player_a_name:
                player_a = p
            if p.name() == player_b_name:
                player_b = p
        if player_a is None:
            player_a = Player(player_a_name)
        if player_b is None:
            player_b = Player(player_b_name)
        self.add_result(player_a, player_b, wins_a, wins_b)

    def add_bye(self, player):
        assert(False)

    def players(self):
        players_a = [rslt._player_a for rslt in self._match_log];
        players_b = [rslt._player_b for rslt in self._match_log];
        return set(players_a + players_b)

    def times_matched(self, player_a, player_b):
        rslt = 0
        for entry in self._match_log:
            if entry.has_players(player_a, player_b):
                rslt += 1
        return rslt

    def players_match_wins(self):
        rslt = {p: 0 for p in self.players()}
        for entry in self._match_log:
            winner = entry.winner()
            if winner is not None:
                rslt[winner] += 1
        return rslt


    def round_matchups(self):
        mate = nx.max_weight_matching(self._matchup_graph(), \
                                      maxcardinality=True)
        rslt = []
        for k, v in mate:
            if (k, v) not in rslt:
                rslt.append((k, v))

        # Sort pairs by wins
        wins = self.players_match_wins()
        for i, pair in enumerate(rslt):
            if wins[pair[0]] < wins[pair[1]]:
                rslt[i] = (pair[1], pair[0])

        matchups = []
        for e in rslt:
            matchups.append(Matchup(e[0], e[1], \
                                    self._matchup_cost(e[0], e[1])))
        return matchups


    def print_round_matchups(self):
        matchups = self.round_matchups()
        for matchup in matchups:
            vs_str = matchup.player_a.name() \
                     + " VS. " \
                     + matchup.player_b.name()
            print(vs_str)


    def _matchup_cost(self, player_a, player_b):
        match_wins = self.players_match_wins()
        PREV_MATCH_COST = 10000
        return PREV_MATCH_COST * self.times_matched(player_a, player_b) \
            + abs(match_wins[player_a] - match_wins[player_b])


    def _matchup_graph(self):
        players = list(self.players())
        graph = nx.Graph()
        for p in players:
            graph.add_node(p)
        for i, pa in enumerate(players):
            for j, pb in enumerate(players):
                if j < i and pa.is_active() and pb.is_active():
                    cost = self._matchup_cost(pa, pb)
                    graph.add_edge(pa, pb, weight=-cost)
        return graph
