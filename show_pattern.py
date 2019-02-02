from test_utilities import *

# r1 pairigs, THEN r1 standings, THEN r2 pairings

r1_standings = standings_from_file('regression_data/mtg/swedish_championships_day_1_round_1_standings.csv')

player_to_standing = dict()
for i,row in enumerate(r1_standings):
    player_to_standing[row[0]] = i

r2_pairings = pairings_from_file('regression_data/mtg/swedish_championship_day_1_round_2_pairings.csv')

for pair in r2_pairings:
    print(player_to_standing[pair[0]], \
          ' vs ',
          player_to_standing[pair[1]], \
          '(', pair[0], ' vs ', pair[1], ')')
