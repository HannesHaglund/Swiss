class Matchup:
    def __init__(self, player_a, player_b, cost):
        self.player_a = player_a
        self.player_b = player_b
        self.cost = cost


    def string(self):
        return (self.player_a.name() + " VS. " + \
                self.player_b.name())


    def is_bye(self):
        return player_b is None



class Matchups:
    def __init__(self):
        self.pairs = []
        self.bye_player = None


    def players_are_matched(self, pa, pb):
        for m in self.pairs:
            if (m.player_a == pa and m.player_b == pb or \
                m.player_a == pb and m.player_b == pa):
                return True
        return False


    def badness(self):
        return sum([m.cost for m in self.pairs])


    def badness_values(self, word_size):
        def _conv_num(b):
            word_max = 2**word_size
            rslt = []
            while b > 0:
                rslt.insert(0, b % word_max)
                b = b >> word_size
            return rslt
        print(_conv_num(1))
        print(_conv_num(2**65))
        for m in self.pairs:
            print(_conv_num(m.cost), m.player_a.name(), m.player_b.name())
        return _conv_num(self.badness())


    def string(self):
        rslt = ""
        for matchup in self.pairs:
            rslt += matchup.string() + linesep
        if self.bye_player is not None:
            rslt += (self.bye_player.name() + " gets a bye." + linesep)
        return rslt.rstrip() # Remove last endline


def matchups_from_tuple_list(tuple_list, cost_map):
    ms = Matchups()
    for entry in tuple_list:
        player_a = entry[0]
        player_b = entry[1]
        cost = cost_map[player_a][player_b]
        ms.pairs.append(Matchup(player_a, player_b, cost))
    return ms
