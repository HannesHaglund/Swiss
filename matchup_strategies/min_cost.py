import networkx as nx
import random
import math
import itertools
from tournament import Matchups, Matchup
from match_log import MatchLog
from player import Player

def pairings(tournament):
    """
    Generate pairings where pairings are optimized according to the following qualities, in order of importance:
    1. Minimize times opponents have previously faced each other
    2. Minimize difference in wins between opponents

    If the number of players is odd, a bye player is chosen according to the following criteria, in order of importance:
    1. Minimize times gotten bye before of bye player
    2. Minimize number of wins of bye player
    3. Minimize cost of other matchups
    """

    match_log = tournament.match_log()
    players = tournament.players()

    # Asserts should fail if this is exceeded
    MAX_ROUND_ROBINS = 1000
    maxWinDiff = (len(players) + 1) * MAX_ROUND_ROBINS

    # Larger than any cost due to win differences
    prevMatchCost = maxWinDiff + 1
    # Larger than any possible _matchup_cost
    byeWinMultiplier = prevMatchCost*MAX_ROUND_ROBINS + maxWinDiff + 1
    # Huge
    byeByeMultiplier = byeWinMultiplier * MAX_ROUND_ROBINS + 1

    DUMMY_PLAYER_FOR_BYE_MATCHUP = Player("")

    if len(players) == 0:
        return Matchups()

    def _matchup_cost(player_a, player_b):
        a_wins = match_log.times_match_win(player_a)
        b_wins = match_log.times_match_win(player_b)
        wins_diff = abs(a_wins - b_wins)
        times_played = match_log.times_matched(player_a, player_b)
        cost = prevMatchCost * times_played + wins_diff
        assert(times_played < MAX_ROUND_ROBINS)
        assert(wins_diff < maxWinDiff)
        assert(wins_diff + 1 < prevMatchCost)
        assert(cost < byeWinMultiplier)
        return cost

    def _gen_graph_without_edges():
        graph = nx.Graph()
        for p in players:
            graph.add_node(p)
        return graph

    def _add_matchup_cost_edges_to_graph(graph):
        max_extra_randomness = 0.99 / len(players)
        for i, pa in enumerate(players):
            for j, pb in enumerate(players):
                if (j < i and pa.is_active() and pb.is_active()):
                    # Ensure random result if multiple optimums exist
                    randomness = random.uniform(0, max_extra_randomness)
                    cost = _matchup_cost(pa, pb) + randomness
                    graph.add_edge(pa, pb, weight=-cost)
        return graph

    def _add_bye_node_to_graph(graph):
        graph.add_node(DUMMY_PLAYER_FOR_BYE_MATCHUP)
        for p in players:
            wins = match_log.times_match_win(p)
            byes = match_log.times_got_bye(p)
            c = wins * byeWinMultiplier + \
                byes * byeByeMultiplier
            assert(byeByeMultiplier > byeWinMultiplier)
            assert(c == 0 or c >= byeWinMultiplier)
            graph.add_edge(p, DUMMY_PLAYER_FOR_BYE_MATCHUP, weight=-c)
        return graph

    def _pairs_from_graph(graph):
        mate = nx.max_weight_matching(graph, maxcardinality=True)
        # Extract pairs
        matched_players = []
        pairs = []
        for k, v in mate:
            if (k, v) not in pairs:
                pairs.append((k, v))
        # Sort pairs by wins
        for i, pair in enumerate(pairs):
            wins_zero = match_log.times_match_win(pair[0])
            wins_one = match_log.times_match_win(pair[1])
            if wins_zero < wins_one:
                pairs[i] = (pair[1], pair[0])
        # Format as matchups
        matchups = Matchups()
        for e in pairs:
            cost = _matchup_cost(e[0], e[1])
            if e[0] == DUMMY_PLAYER_FOR_BYE_MATCHUP:
                assert(matchups.bye_player is None)
                matchups.bye_player = e[1]
            elif e[1] == DUMMY_PLAYER_FOR_BYE_MATCHUP:
                assert(matchups.bye_player is None)
                matchups.bye_player = e[0]
            else:
                matchups.pairs.append(Matchup(e[0], e[1], cost))
        # Set bye player
        return matchups

    graph = _gen_graph_without_edges()
    graph = _add_matchup_cost_edges_to_graph(graph)
    if len(players) % 2 != 0:
        graph = _add_bye_node_to_graph(graph)

    matchups = _pairs_from_graph(graph)
    return matchups


def number_of_possible_pairings(tournament):
    players = tournament.players()
    match_log = tournament.match_log()

    if len(players) == 0:
        return 1

    def _matchup_cost(player_a, player_b):
        # Asserts should fail after this point
        MAX_ROUND_ROBINS = 1000
        maxWinDiff = (len(players) + 1) * MAX_ROUND_ROBINS
        # Larger than any cost due to win differences
        prevMatchCost = maxWinDiff + 1
        # Calculate cost
        a_wins = match_log.times_match_win(player_a)
        b_wins = match_log.times_match_win(player_b)
        wins_diff = abs(a_wins - b_wins)
        times_played = match_log.times_matched(player_a, player_b)
        cost = prevMatchCost * times_played + wins_diff
        assert(times_played < MAX_ROUND_ROBINS)
        assert(wins_diff < maxWinDiff)
        assert(wins_diff + 1 < prevMatchCost)
        return cost

    def _best_bye_candidates():
        if len(players) % 2 == 0:
            return []
        ranking = tournament.rank_score_pairs() # Contains active players only
        min_byes = tournament.match_log().min_active_bye_count()
        ranking_of_byeable = [e \
                             for e in ranking \
                             if tournament.match_log().times_got_bye(e[1]) == min_byes]
        lowest_score = min([e[0] for e in ranking_of_byeable])
        lowest_scoring_players = [player \
                                  for (score, player) in ranking_of_byeable \
                                  if score <= lowest_score]
        return lowest_scoring_players

    # Brute force
    an_optimal_matchup = pairings(tournament)
    optimal_badness = math.floor(an_optimal_matchup.badness())
    bye_candidates = _best_bye_candidates()
    perms = list(itertools.permutations(tournament.players()))
    pair_permutations_count = math.factorial(math.floor(len(tournament.players()) / 2))

    if len(perms) == 1:
        return 1

    rslt = 0

    for perm in perms:
        # Check for legal bye player and ignore him
        if len(tournament.players()) % 2 == 1:
            if perm[-1] not in bye_candidates:
                continue
            perm = perm[:-1]

        # Extract every two elements
        assert(len(perm) % 2 == 0)
        every_two_elements = []
        for i in range(round(len(perm) / 2)):
            every_two_elements.append((perm[2*i], perm[2*i+1]))

        # Remove perm with only internal order changed
        if any([a.name() < b.name() for (a, b) in every_two_elements]):
            continue

        # Calculate badness
        badness = 0
        for a,b in every_two_elements:
            badness += _matchup_cost(a, b)

        # Is badness optimal?
        assert(badness >= optimal_badness)
        if badness == optimal_badness:
            # Since there can be different permutations of two-pairs,
            # we'll get to this point n! times, where n is len(every_two_elements)
            rslt += 1 / pair_permutations_count

    assert(abs(rslt - round(rslt)) < 0.01)
    return round(rslt)
