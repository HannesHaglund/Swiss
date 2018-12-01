from matchup_optimization import optimal_matchup, number_of_optimal_matchups
from matchup_cost_map import matchup_cost_map
from player import bye_dummy

def _matchup_cost_functions(match_log):
    def _times_bye(player_a, player_b):
        if (player_a == bye_dummy()):
            return match_log.times_got_bye(player_b)
        elif (player_b == bye_dummy()):
            return match_log.times_got_bye(player_a)
        else:
            return 0

    def _bye_player_wins(player_a, player_b):
        if (player_a == bye_dummy()):
            return match_log.times_match_win(player_b)
        elif (player_b == bye_dummy()):
            return match_log.times_match_win(player_a)
        else:
            return 0

    def _times_faced(player_a, player_b):
        return match_log.times_matched(player_a, player_b)

    def _win_diff(player_a, player_b):
        return abs(match_log.times_match_win(player_a) - match_log.times_match_win(player_b))

    return [_times_bye, _bye_player_wins, _times_faced, _win_diff]


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
    players = tournament.players() + \
              ([bye_dummy()] if len(tournament.players()) % 2 == 1 else [])
    cost_functions = _matchup_cost_functions(tournament.match_log())
    return optimal_matchup(tournament, \
                           matchup_cost_map(players, cost_functions))


def number_of_possible_pairings(tournament):
    players = tournament.players() + \
              ([bye_dummy()] if len(tournament.players()) % 2 == 1 else [])
    cost_functions = _matchup_cost_functions(tournament.match_log())
    return number_of_optimal_matchups(tournament, \
                                      matchup_cost_map(players, cost_functions))
