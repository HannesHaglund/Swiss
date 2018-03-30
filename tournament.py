import networkx as nx
import random
import operator
from player import Player

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
    _match_log = []


    def add_result(self, player_a, player_b, wins_a, wins_b):
        self._match_log.append(MatchResult(player_a, player_b, wins_a, wins_b))


    def add_result_by_names(self, player_a_name, player_b_name, wins_a, wins_b):
        player_a = self._player_name_player(player_a_name)
        player_b = self._player_name_player(player_b_name)
        self.add_result(player_a, player_b, wins_a, wins_b)


    def add_bye(self, player):
        self._match_log.append(MatchResult(player, None, 0, 0))


    def add_bye_by_name(self, player_name):
        player = self._player_name_player(player_name)
        self.add_bye(player)


    def players(self):
        players_a = [e._player_a \
                     for e in self._match_log \
                     if e._player_a is not None];
        players_b = [e._player_b \
                     for e in self._match_log \
                     if e._player_b is not None];
        return set(players_a + players_b)


    def times_matched(self, player_a, player_b):
        rslt = 0
        for entry in self._match_log:
            if entry.has_players(player_a, player_b):
                rslt += 1
        return rslt


    def times_got_bye(self, player):
        rslt = 0
        for entry in self._match_log:
            if entry.is_bye() and entry.winner() == player:
                rslt += 1
        return rslt


    def players_match_wins(self):
        rslt = {p: 0 for p in self.players()}
        for entry in self._match_log:
            winner = entry.winner()
            if winner is not None:
                rslt[winner] += 1
        return rslt


    def ranking(self):
        pairs_by_win = self._rank_score_pairs()
        ranked_players = [e[0] for e in pairs_by_win]
        return ranked_players


    def round_matchups(self):
        bye = self._bye_player()
        mate = nx.max_weight_matching(self._matchup_graph(bye), \
                                      maxcardinality=True)

        # Extract data
        matched_players = []
        pairs = []
        for k, v in mate:
            matched_players.append(k)
            if (k, v) not in pairs:
                pairs.append((k, v))

        # Sort pairs by wins
        wins = self.players_match_wins()
        for i, pair in enumerate(pairs):
            if wins[pair[0]] < wins[pair[1]]:
                pairs[i] = (pair[1], pair[0])

        # Format as matchups
        matchups = Matchups()
        for e in pairs:
            cost = self._matchup_cost(e[0], e[1])
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


    def _rank_score_pairs(self):
        match_wins = self.players_match_wins()
        pairs_by_name = sorted(match_wins.items(), \
                               key=lambda e: e[0].name())
        pairs_by_win = sorted(match_wins.items(), \
                              key=operator.itemgetter(1))
        pairs_by_win.reverse() # Best to worst
        return [e for e in pairs_by_win if e[0].is_active()]


    def _player_name_player(self, player_name):
        players = self.players()
        player = None
        for p in players:
            if p.name() == player_name:
                player = p
                break
        if player is None:
            player = Player(player_name)
        return player


    def _active_player_count(self):
        players = self.players()
        rslt = 0
        for p in players:
            if p.is_active():
                rslt += 1
        return rslt


    def _min_active_bye_count(self):
        byes = []
        players = self.players()
        for p in players:
            if p.is_active():
                byes.append(self.times_got_bye(p))
        if len(byes) == 0:
            return 0
        else:
            return min(byes)


    def _bye_player(self):
        """Returns the lowest ranked active player"""
        if self._active_player_count() % 2 == 0:
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


    def _matchup_cost(self, player_a, player_b):
        match_wins = self.players_match_wins()
        PREV_MATCH_COST = 10000
        return PREV_MATCH_COST * self.times_matched(player_a, player_b) \
            + abs(match_wins[player_a] - match_wins[player_b])


    def _matchup_graph(self, bye_player):
        players = list(self.players())
        graph = nx.Graph()
        for p in players:
            graph.add_node(p)
        for i, pa in enumerate(players):
            for j, pb in enumerate(players):
                if (j < i and \
                    (pa.is_active() and pb.is_active()) and \
                    (pa != bye_player and pb != bye_player)):

                    cost = self._matchup_cost(pa, pb) +\
                           random.uniform(0, 0.99)
                    graph.add_edge(pa, pb, weight=-cost)
        return graph
