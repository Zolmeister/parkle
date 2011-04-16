## Parkel 0.0

class Parkel(object):
    def __init__(self):
        self.goal = 10000
        self.players = []
    
    def roll(n):
        """Return list of n random numbers from 1 to 6."""
        pass

    def start_game():
        pass
    
    def turn(player):
        pass
    
    def determine_points(kept):
        """Return number of points represented."""
        pass

class Player(object):
    def __init__(self):
        self.game = None
        self.name = ""
        self.score = 0;
        self.kept = [];

    def decide(self, dice):
        """Return number of dice left to roll."""
        return 0

class RealPlayer(Player):
    pass
