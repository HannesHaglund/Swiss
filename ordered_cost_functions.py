

class OrderedCostFunctions:
    def __init__(self):
        self.cost_functions = []
        self.bits_occupied = []


    def append(self, func, bits_occupied=32):
        self.cost_functions.append(func)
        self.bits_occupied.append(bits_occupied)


    def adjust_max_numbers(self, players):
        # Adjust max_numbers so self.cost can be ran for all players in players
        for pa in players:
            for pb in players:
                if pa == pb:
                    continue
                for i in range(len(self.cost_functions)):
                    while (self.cost_functions[i](pa, pb) > \
                           self._max_cost_of_func(i)):
                        self.bits_occupied[i] += 1
        # Assert that we can handle all players without issues
        for pa in players:
            for pb in players:
                self.cost(pa, pb)
        # Cost functions should be symmetrical
        for pa in players:
            for pb in players:
                assert(self.cost(pa, pb) == self.cost(pb, pa))


    def cost(self, player_a, player_b):
        result = 0
        for i in range(len(self.cost_functions)):
            max_cost = self.bits_occupied[i]
            cost = self.cost_functions[i](player_a, player_b)
            assert(cost >= 0)
            assert(cost <= self._max_cost_of_func(i))
            assert(round(cost) == cost)
            result = (result << self.bits_occupied[i])
            result += cost
        return result


    def _max_cost_of_func(self, func_index):
        return 2**self.bits_occupied[func_index] - 1
