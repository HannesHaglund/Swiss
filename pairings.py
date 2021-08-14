import os

class Pairing:
    def __init__(self, player_a, player_b, cost):
        self.player_a = player_a
        self.player_b = player_b
        self.cost = cost


    def string(self):
        return (self.player_a + " VS. " + self.player_b)


    def is_bye(self):
        return player_b is None



class Pairings:
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


    def string(self):
        rslt = ""
        for pairing in self.pairs:
            rslt += pairing.string() + os.linesep
        if self.bye_player is not None:
            rslt += (self.bye_player + " gets a bye." + os.linesep)
        return rslt.rstrip() # Remove last endline
