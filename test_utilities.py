import csv
from tournament import Tournament
from player import Player

def pairings_from_file(fname):
    rslt = []
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if row[0][0] == '#':
                continue
            # Player a, player b
            rslt.append( (row[1], row[2]) )
        return rslt
    raise Exception('Read failure')

def standings_from_file(fname):
    rslt = []
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if row[0][0] == '#':
                continue
            # Player, score
            rslt.append( ( row[1], int(row[2]) ) )
        return rslt
    raise Exception('Read failure')

def swedish_championship_tournament_and_wanted_pairings():
    """
    Return a tournament along with wanted pairings for next round in the form
    of a list of tuple pairs.
    """

    standings_round_1 = standings_from_file('regression_data/mtg/swedish_championships_day_1_round_1_standings.csv')

    def _r1_winners():
        rslt = []
        for row in standings_round_1:
            if row[1] > 0: # If won
                rslt.append(row[0]) # Append player name
        return rslt

    r1_winners = _r1_winners()
    standings_round_2 = standings_from_file('regression_data/mtg/swedish_championships_day_1_round_2_standings.csv')

    def _r2_winners():
        rslt = []
        for row in standings_round_2:
            if row[1] != 1 and row[1] != 3 and row[0] not in r1_winners:
                rslt.append(row[0])
        return rslt

    r2_winners = _r2_winners()

    r1_pairings = pairings_from_file('regression_data/mtg/swedish_championship_day_1_round_1_pairings.csv')
    r2_pairings = pairings_from_file('regression_data/mtg/swedish_championship_day_1_round_2_pairings.csv')

    t = Tournament()
    for row in standings_round_2:
        t.add_player(Player(row[0]))

    for pair in r1_pairings:
        if pair[0] in r1_winners and pair[1] in r1_winners:
            t.add_result_by_names(pair[0], pair[1], 1, 1)
        elif pair[0] in r1_winners:
            t.add_result_by_names(pair[0], pair[1], 3, 0)
        elif pair[1] in r1_winners:
            t.add_result_by_names(pair[0], pair[1], 0, 3)

    for pair in r2_pairings:
        if pair[0] in r2_winners and pair[1] in r2_winners:
            t.add_result_by_names(pair[0], pair[1], 1, 1)
        elif pair[0] in r2_winners:
            t.add_result_by_names(pair[0], pair[1], 3, 0)
        elif pair[1] in r2_winners:
            t.add_result_by_names(pair[0], pair[1], 0, 3)

    r3_pairings = pairings_from_file('regression_data/mtg/swedish_championship_day_1_round_3_pairings.csv')

    return (t, r3_pairings)
