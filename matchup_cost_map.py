import math
import itertools

def matchup_cost_map(players, cost_functions):
    """
    Create a mapping between player pairs and a cost for matchup said player pair.

    The absolute size of these costs are arbitrary, but their relative size is not.

    The cost is determined by cost_functions, a list of functions, each taking two
    players as argument. Each function following after the first acts as a
    tie-breaker if should previous cost functions return the same values when
    choosing from different matchups.

    Return a dict such that:
    dict[pa][pb] = cost
    for any combination pa or pb in players.
    """

    if len(players) == 0:
        return dict()

    num_pairings_in_round = math.ceil(len(players)/2)
    all_possible_pairs = list(itertools.combinations(players, 2))

    def _init_cost_map():
        cost_map = dict()
        for p in players:
            cost_map[p] = dict()
            for pb in players:
                if pb != p:
                    cost_map[p][pb] = 0
        return cost_map

    def _set_cost(cost_map, pa, pb, cost):
        cost_map[pa][pb] = cost
        cost_map[pb][pa] = cost

    def _eval_cost_functions(pa, pb, bits_per_func):
        result = 0
        max_cost = 2**bits_per_func - 1
        for i in range(len(cost_functions)):
            cost = cost_functions[i](pa, pb)
            assert(cost >= 0)
            assert(cost * num_pairings_in_round <= max_cost)
            assert(round(cost) == cost)
            result = (result << bits_per_func)
            result += cost
        return result

    def _assert_two_of_each_value(cost_map):
        values = [v for (k,v) in cost_map.items()]
        for v in values:
            assert(values.count(v) == 1)

    cost_map = _init_cost_map()
    max_bits = 64
    for (pa, pb) in all_possible_pairs:
        _set_cost(cost_map, pa, pb, _eval_cost_functions(pa, pb, max_bits))
    for (pa, pb) in all_possible_pairs:
        assert(cost_map[pa][pb] == cost_map[pb][pa])
    _assert_two_of_each_value(cost_map)

    return cost_map
