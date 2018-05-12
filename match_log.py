import networkx as nx
import random
import operator


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


    def times_match_win(self, player):
        rslt = 0
        for entry in self._entries:
            winner = entry.winner()
            if winner == player:
                rslt += 1
        return rslt


    def rank_score_pairs(self, unlogged_players=[]):
        active_unlogged = [p for p in unlogged_players \
                           if p.is_active()]
        players = self.active_players() + active_unlogged
        score_player_pairs = [(self.times_match_win(p), p) \
                              for p in players]
        pairs_by_name = sorted(score_player_pairs, \
                               key=lambda e: e[0].name())
        pairs_by_win = sorted(match_wins.items(), \
                              key=operator.itemgetter(1))
        pairs_by_win.reverse() # Best to worst
        return [e for e in pairs_by_win if e[0].is_active()]


    def best_bye_candidate(self):
        if len(self.active_players()) % 2 == 0:
            return None
        ranking = self.rank_score_pairs() # Contains active only
        lowest_score = min([e[1] for e in ranking])
        lowest_scoring_players = [player \
                                  for (player, score) in ranking \
                                  if score <= lowest_score]
        min_byes = self._min_active_bye_count()
        byeable_players = [p for p in lowest_scoring_players \
                           if self.times_got_bye(p) == min_byes]
        return random.choice(byeable_players)


    def matchup_graph(self, extra_players=[], bye_player=None):
        players = list(set(list(self.players()) + extra_players))
        if bye_player is not None and bye_player not in players:
            players.append(bye_player)
        graph = nx.Graph()
        for p in players:
            graph.add_node(p)
        for i, pa in enumerate(players):
            for j, pb in enumerate(players):
                if (j < i and \
                    (pa.is_active() and pb.is_active()) and \
                    (pa != bye_player and pb != bye_player)):

                    # Ensure random result if multiple optimums exist
                    cost = self.matchup_cost(pa, pb) +\
                           random.uniform(0, 0.99)

                    graph.add_edge(pa, pb, weight=-cost)
        return graph


    def matchup_cost(self, player_a, player_b):
        a_wins = self.times_match_win(player_a)
        b_wins = self.times_match_win(player_b)
        wins_diff = abs(a_wins - b_wins)
        times_played = self.times_matched(player_a, player_b)
        PREV_MATCH_COST = 10000
        return PREV_MATCH_COST * times_played + wins_diff


    def _min_active_bye_count(self):
        byes = []
        players = self.active_players()
        for p in players:
            byes.append(self.times_got_bye(p))
        if len(byes) == 0:
            return 0
        else:
            return min(byes)
