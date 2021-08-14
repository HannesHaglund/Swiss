import networkx as nx
import math
import itertools
from pairings import Pairing, Pairings
from match_log import MatchLog
from shared_functions import bye_dummy_player_name

def optimal_pairing(match_log, cost_map):
    players = match_log.players()
    if len(players) % 2 != 0:
        players.append(bye_dummy_player_name())

    if len(players) == 0:
        return Pairings()

    def _gen_graph_without_edges():
        graph = nx.Graph()
        for p in players:
            graph.add_node(p)
        return graph

    def _add_pairing_cost_edges_to_graph(graph):
        done_costs = set()
        for i, pa in enumerate(players):
            for j, pb in enumerate(players):
                if (j < i and match_log.is_player_active(pa) and match_log.is_player_active(pb)):
                    cost = cost_map[pa][pb]
                    if cost in done_costs:
                        raise Exception("cost_map does not return unique values")
                    done_costs.add(cost)
                    graph.add_edge(pa, pb, weight=-cost)
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
        # Format as pairings
        pairings = Pairings()
        for e in pairs:
            cost = cost_map[e[0]][e[1]]
            if e[0] == bye_dummy_player_name():
                assert(pairings.bye_player is None)
                pairings.bye_player = e[1]
            elif e[1] == bye_dummy_player_name():
                assert(pairings.bye_player is None)
                pairings.bye_player = e[0]
            else:
                num_0 = players.index(e[0])
                num_1 = players.index(e[1])
                player_a = e[0] if num_0 < num_1 else e[1]
                player_b = e[1] if player_a == e[0] else e[0]
                pairings.pairs.append(Pairing(player_a, player_b, cost))
        # Set bye player
        return pairings

    graph = _gen_graph_without_edges()
    graph = _add_pairing_cost_edges_to_graph(graph)
    return _pairs_from_graph(graph)


def number_of_optimal_pairings(match_log, cost_map):
    players = match_log.players()
    if len(players) % 2 != 0:
        players.append(bye_dummy_player_name())
    # Brute force
    possible_pairings_in_round = round(len(players) / 2) # Always even
    perms = itertools.permutations(players)
    pairs_costs = []
    for perm in perms:
        cost = 0
        for i in range(possible_pairings_in_round):
            pa = perm[i*2]
            pb = perm[i*2 + 1]
            cost += cost_map[pa][pb]
        pairs_costs.append(cost)
    min_cost = min(pairs_costs)
    s = sum([1 if c == min_cost else 0 for c in pairs_costs])
    rslt = s / (math.factorial(possible_pairings_in_round) * 2**possible_pairings_in_round)
    assert(round(rslt) == rslt)
    return round(rslt)
