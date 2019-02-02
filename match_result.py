class MatchResult:
    def __init__(self, player_a, player_b, wins_a, wins_b):
        self._player_a = player_a
        self._player_b = player_b
        self._player_a_wins = wins_a
        self._player_b_wins = wins_b


    def has_players(self, player_a, player_b):
        return ((self._player_a == player_a and self._player_b == player_b) \
            or (self._player_a == player_b and self._player_b == player_a))


    def game_wins_of(self, player):
        if self._player_a == player:
            return self._player_a_wins
        if self._player_b == player:
            return self._player_b_wins
        return 0


    def is_bye(self):
        return (self._player_a is None or \
                self._player_b is None)


    def winner(self):
        if (self._player_a is not None and \
            self._player_b is None):
            return self._player_a
        if (self._player_b is not None and \
            self._player_a is None):
            return self._player_b
        if self._player_a_wins > self._player_b_wins:
            return self._player_a
        if self._player_b_wins > self._player_a_wins:
            return self._player_b
        return None
