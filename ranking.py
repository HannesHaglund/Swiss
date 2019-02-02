from os import linesep

class RankingEntry:
    def __init__(self, player, score, rank):
        self._player = player
        self._score = score
        self._rank = rank


    def rank(self):
        return self._rank


    def player(self):
        return self._player


    def score(self):
        return self._score



class Ranking:
    def __init__(self):
        self._entries = []


    def add_entry(self, player, score):
        self._entries.append(RankingEntry(player, score, 0))
        # Sort in proper order
        self._entries = sorted(self._entries, key=lambda e: e.player().name())
        self._entries = sorted(self._entries, key=lambda e: e.score())
        self._entries.reverse() # Best to worst
        for i,e in enumerate(self._entries):
            e._rank = i+1


    def entries(self):
        return self._entries


    def string(self):
        rslt = ""
        max_name_length = max([len(entry.player().name()) for entry in self._entries])
        max_numerals = len(str(self._entries[-1].rank()))
        for i,entry in enumerate(self._entries):
            layout = "#{:<" + str(max_numerals) + "}: {: <" + str(max_name_length) + "} {}"
            cols = [str(i+1), entry.player().name(), "("+str(entry.score())+" wins)"]
            rslt += layout.format(*cols)
            rslt += linesep
        return rslt
