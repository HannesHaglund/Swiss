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
