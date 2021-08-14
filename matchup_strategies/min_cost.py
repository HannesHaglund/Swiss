from matchup_optimization import optimal_matchup, number_of_optimal_matchups
from matchup_cost_map import matchup_cost_map
from shared_functions import bye_dummy_player_name

def _matchup_cost_functions(match_log):

    def _minimize_times_bye(player_a, player_b):
        if (player_a == bye_dummy_player_name()):
            return match_log.times_got_bye(player_b)
        elif (player_b == bye_dummy_player_name()):
            return match_log.times_got_bye(player_a)
        else:
            return 0

    def _minimize_bye_player_wins(player_a, player_b):
        if (player_a == bye_dummy_player_name()):
            return match_log.times_match_win(player_b)
        elif (player_b == bye_dummy_player_name()):
            return match_log.times_match_win(player_a)
        else:
            return 0

    def _minimize_times_matched(player_a, player_b):
        return match_log.times_matched(player_a, player_b)

    def _minimize_win_diff(player_a, player_b):
        return abs(match_log.times_match_win(player_a) - match_log.times_match_win(player_b))

    def _minimize_player_number_diff(player_a, player_b):
        num_a = match_log.players().index(player_a)
        num_b = match_log.players().index(player_b)
        return abs(num_a - num_b)

    def _maximize_player_number_sum(player_a, player_b):
        players = match_log.players()
        player_count = len(players)
        num_a = players.index(player_a)
        num_b = players.index(player_b)
        return 2*player_count - (num_a + num_b)

    return [_minimize_times_bye, \
            _minimize_bye_player_wins, \
            _minimize_times_matched, \
            _minimize_win_diff, \
            _minimize_player_number_diff, \
            _maximize_player_number_sum]

def pairings(match_log):
    """
    Generate pairings where pairings are optimized according to the following qualities, in order of importance:
    1. Minimize times opponents have previously faced each other
    2. Minimize difference in wins between opponents

    If the number of players is odd, a bye player is chosen according to the following criteria, in order of importance:
    1. Minimize times gotten bye before of bye player
    2. Minimize number of wins of bye player
    3. Minimize cost of other matchups
    """
    players = match_log.players()
    cost_functions = _matchup_cost_functions(match_log)
    return optimal_matchup(match_log, \
                           matchup_cost_map(players, cost_functions))


def number_of_possible_pairings(match_log):
    players = match_log.players()
    cost_functions = _matchup_cost_functions(match_log)
    return number_of_optimal_matchups(match_log, \
                                      matchup_cost_map(players, cost_functions))
