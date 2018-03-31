import networkx as nx
import random


class MatchResult:
    _player_a = None
    _player_b = None
    _player_a_wins = 0
    _player_b_wins = 0


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


    def __init__(self, player_a, player_b, wins_a, wins_b):
        self._player_a = player_a
        self._player_b = player_b
        self._player_a_wins = wins_a
        self._player_b_wins = wins_b


class MatchLog:
    _entries = []


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
        return set(players_a + players_b)


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


    def players_match_wins(self):
        rslt = {p: 0 for p in self.players()}
        for entry in self._entries:
            winner = entry.winner()
            if winner is not None:
                rslt[winner] += 1
        return rslt


    def ranking(self):
        pairs_by_win = self._rank_score_pairs()
        ranked_players = [e[0] for e in pairs_by_win]
        return ranked_players


    def best_bye_candidate(self):
        if len(self.active_players()) % 2 == 0:
            return None
        players = self.players()
        ranking = self._rank_score_pairs() # Contains active only
        lowest_score = min([e[1] for e in ranking])
        lowest_scoring_players = [player \
                                  for (player, score) in ranking \
                                  if score <= lowest_score]
        min_byes = self._min_active_bye_count()
        byeable_players = [p for p in lowest_scoring_players \
                           if self.times_got_bye(p) == min_byes]
        return random.choice(byeable_players)


    def matchup_graph(self, bye_player=None):
        players = list(self.players())
        graph = nx.Graph()
        for p in players:
            graph.add_node(p)
        for i, pa in enumerate(players):
            for j, pb in enumerate(players):
                if (j < i and \
                    (pa.is_active() and pb.is_active()) and \
                    (pa != bye_player and pb != bye_player)):

                    cost = self.matchup_cost(pa, pb) +\
                           random.uniform(0, 0.99)
                    graph.add_edge(pa, pb, weight=-cost)
        return graph


    def matchup_cost(self, player_a, player_b):
        match_wins = self.players_match_wins()
        PREV_MATCH_COST = 10000
        return PREV_MATCH_COST * self.times_matched(player_a, player_b) \
            + abs(match_wins[player_a] - match_wins[player_b])


    def _rank_score_pairs(self):
        match_wins = self.players_match_wins()
        pairs_by_name = sorted(match_wins.items(), \
                               key=lambda e: e[0].name())
        pairs_by_win = sorted(match_wins.items(), \
                              key=operator.itemgetter(1))
        pairs_by_win.reverse() # Best to worst
        return [e for e in pairs_by_win if e[0].is_active()]


    def _min_active_bye_count(self):
        byes = []
        players = self.active_players()
        for p in players:
            byes.append(self.times_got_bye(p))
        if len(byes) == 0:
            return 0
        else:
            return min(byes)
