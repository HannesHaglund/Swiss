class Player:
    def __init__(self, name):
        self._name = name
        self._active = True


    def name(self):
        return self._name


    def is_active(self):
        return self._active


    def leave(self):
        self._active = False


    def reenter(self):
        self._active = True


# Special player, used to be matched up with player who is to be byed
_bye_dummy = Player("BYE_PLAYER_ac2da556-27ad-4323-b5cc-f3eab047ed97")

def bye_dummy():
    return _bye_dummy
