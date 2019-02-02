from matchup_optimization import optimal_matchup, number_of_optimal_matchups
from matchup_cost_map import matchup_cost_map
from player import bye_dummy

def _matchup_cost_functions(tournament):

    match_log = tournament.match_log()

    def _minimize_times_bye(player_a, player_b):
        if (player_a == bye_dummy()):
            return match_log.times_got_bye(player_b)
        elif (player_b == bye_dummy()):
            return match_log.times_got_bye(player_a)
        else:
            return 0

    def _minimize_bye_player_wins(player_a, player_b):
        if (player_a == bye_dummy()):
            return match_log.times_game_win(player_b)
        elif (player_b == bye_dummy()):
            return match_log.times_game_win(player_a)
        else:
            return 0

    def _minimize_times_matched(player_a, player_b):
        return match_log.times_matched(player_a, player_b)

    def _minimize_win_diff(player_a, player_b):
        return abs(match_log.times_game_win(player_a) - match_log.times_game_win(player_b))

    def _minimize_player_number_diff(player_a, player_b):
        num_a = tournament.player_number_of_player(player_a)
        num_b = tournament.player_number_of_player(player_b)
        return abs(num_a - num_b)

    def _maximize_player_number_sum(player_a, player_b):
        player_count = len(tournament.players())
        num_a = tournament.player_number_of_player(player_a)
        num_b = tournament.player_number_of_player(player_b)
        return 2*player_count - (num_a + num_b)

    return [_minimize_times_bye, \
            _minimize_bye_player_wins, \
            _minimize_times_matched, \
            _minimize_win_diff, \
            _minimize_player_number_diff, \
            _maximize_player_number_sum]

def cost_map(tournament):
    players = tournament.players() + \
              ([bye_dummy()] if len(tournament.players()) % 2 == 1 else [])
    cost_functions = _matchup_cost_functions(tournament)
    return matchup_cost_map(players, cost_functions)

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
    return optimal_matchup(tournament, cost_map(tournament))


def number_of_possible_pairings(tournament):
    return number_of_optimal_matchups(tournament, cost_map(tournament))
