import networkx as nx
import random
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
            if m.player_a == pa and m.player_b == pb:
                return True
            if m.player_a == pb and m.player_b == pa:
                return True
        return False


class Tournament:
    def __init__(self):
        self._match_log = MatchLog()
        self._players = []


    def add_player(self, player):
        self._update_players([player])


    def add_player_by_name(self, player_name):
        self.add_player(Player(player_name))


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
        if len(self._players) == 0:
            return Matchups()

        bye_player = self._best_bye_candidate()

        # match_log only handles players with match results
        if bye_player is None and len(self._players) % 2 == 1:
            bye_player = random.choice(self._players)

        graph = self._match_log.matchup_graph(self._players, bye_player)
        mate = nx.max_weight_matching(graph, maxcardinality=True)

        # Extract pairs
        matched_players = []
        pairs = []
        for k, v in mate:
            matched_players.append(k)
            if (k, v) not in pairs:
                pairs.append((k, v))

        # Sort pairs by wins
        for i, pair in enumerate(pairs):
            wins_zero = self._match_log.times_match_win(pair[0])
            wins_one = self._match_log.times_match_win(pair[1])
            if wins_zero < wins_one:
                pairs[i] = (pair[1], pair[0])

        # Format as matchups
        matchups = Matchups()
        for e in pairs:
            cost = self._match_log.matchup_cost(e[0], e[1])
            matchups.pairs.append(Matchup(e[0], e[1], cost))
        matchups.bye_player = bye_player

        return matchups


    def _best_bye_candidate(self):
        if len(self._players) % 2 == 0:
            return None
        ranking = self._rank_score_pairs() # Contains active players only
        lowest_score = min([e[0] for e in ranking])
        lowest_scoring_players = [player \
                                  for (score, player) in ranking \
                                  if score <= lowest_score]
        min_byes = self._match_log.min_active_bye_count()
        byeable_players = [p for p in lowest_scoring_players \
                           if self._match_log.times_got_bye(p) == min_byes]
        return random.choice(byeable_players)


    def _rank_score_pairs(self):
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
