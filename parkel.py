## Parkel 0.0

class Parkel(object):
    def __init__(self):
        self.goal = 10000
        self.players = []
    
    def roll(n):
        """Return list of n  (1 <= n <= 6) random numbers from 1 to 6.
        
        Return:
            [[value, number of value], ...]

            [[3, 2], [4, 4]] == Pair of 3s, four 4s.
        """
        pass

    def start_game(self):
        """Return winning player."""

        if len(self.players) == 0:
            return

        for p in players:
            p.game = self
        
        while 1:
            for p in self.players:
                self.turn(p)

            for p in self.players:
                if p.score >= self.goal:
                    return p
    
    def turn(player):
        player.rolls = 0
        player.kept = []
        player.begin_turn()

        n = 6;
        while(1):
            d = self.roll(n);
            player.rolls += 1

            if not self.points_possible(d):
                player.kept = []
                return

            r = player.decide(d)

            if r == 0:
                break

            ## Determine if newest kept-set is valid
            ## If invalid, remove entire new set from kept
            nk = player.kept[-1]
            c = len(nk);

            if not calculate_one_keptset(nk):
                player.kept = player.kept[0:-1]
                continue

            n -= c
            if n == 0:
                n = 6
            elif n < 0 or n > 6:
                player.kept = []
                return

        player.score += self.determine_points(player.kept)
    

    def points_possible(self, dice):
        pass

    def determine_points(self, kept):
        """Return number of points represented."""
        pass

    def calculate_one_keptset(self, kset):
        """Calculate number of points for a single item in a kept set."""
        return 0;

class ParkelPlayer(object):
    def __init__(self):
        self.game = None
        self.name = ""
        self.score = 0;
        self.kept = []; # [[1, 1], [3, 3, 3]] = Pair of 2s kept first roll, triple 3s kept second roll
                        # Each sublist is called a "kept-set"
        self.rolls = 0

    def begin_turn(self):
        """User-defined setup method for the beginning of a turn.
        
        No altering of kept should be done here, only pre-calculations.
        """
        pass

    def decide(self, dice):
        """Append kept-set to kept, return 1 to continue with turn, 0 to stop.
        
        Do NOT:
            Change any scores or roll counts
            Call any methods of a Parkel instance
        
        """
        pass

class RealPlayer(ParkelPlayer):
    def begin_turn(self):
        pass

    def decide(self, dice):
        pass

