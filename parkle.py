## Parkle 0.0
##
## Bradley Zeis
## Zoli Kahn

import random
rand = random.Random()

class ParkleView(object):
    def __init__(self):
        self.game = None
        self.current_player = None
        self.winning_player = None

    def start_game(self):
        self.winning_player = self.game.start_game(self)
        self.end_game()

    def start_turn(self, player):
        pass

    def end_turn(self):
        pass

    def end_game(self):
        pass

    def roll(self, dice):
        pass

    def decide(self):
        pass

    def invalid_decision(self):
        pass


class Parkle(object):
    def __init__(self, view):
        self.view = view
        self.goal = 10000
        self.players = []
    
    def roll(self, n):
        """Return list of n  (1 <= n <= 6) random numbers from 1 to 6.

        Return value will be sorted by increasing value
        
        Return:
            [[value, number of value], ...]

            [[3, 2], [4, 4]] == Pair of 3s, four 4s.
        """
        l = []
        for i in range(0, n):
            l.append(rand.randint(1,6))

        d = []
        for i in range(1, 7):
            c = l.count(i)
            if c == 0:
                continue

            d.append([i, c])
            
        return d

    def start_game(self):
        """Return winning player.
        
        Return: ParklePlayer
        """
        if len(self.players) == 0:
            return None

        view.start_game()

        for p in players:
            p.game = self
        
        rand.seed()
        while 1:
            for p in self.players:
                self.turn(p)

            for p in self.players:
                if p.score >= self.goal:
                    return p
    
    def turn(player):
        view.start_turn(player)
        player.rolls = 0
        player.kept = []
        player.begin_turn()

        n = 6
        s = 0
        while(1):
            d = self.roll(n);
            player.rolls += 1

            view.roll(d)

            if not self.points_possible(d):
                player.kept = []
                return

            r = player.decide(d)
            view.decide()

            if r == 0:
                break

            ## Determine if newest kept-set is valid
            ## If invalid, remove entire new set from kept
            nk = player.kept[-1]
            c = len(nk);

            ks = calculate_on_keptset(nk)
            if not ks:
                self.invalid_decision()
                player.kept = player.kept[0:-1]
                continue
            else:
                s += ks

            n -= c
            if n == 0:
                n = 6
            elif n < 0 or n > 6:
                player.kept = []
                return

        player.score += s
        view.end_turn()

    def points_possible(self, dice):
        """Determine if it is possible to score points with dice.
        
        Return: boolean
        """
        num_pairs = 0
        for i in dice:
            if i[0] == 1 or i[0] == 5:
                return True

            if i[1] >= 3:
                return True

            if i[1] == 2:
                num_pairs += 1

            if num_pairs == 3:
                return True

        return False

    def calculate_one_keptset(self, kset):
        """Calculate number of points for a single item in a kept set.
        
        Return: int
        """
        if len(kset) == 1:
            if kset[0] == 1:
                return 100
            if kset[0] == 5:
                return 50
            return 0

        elif len(kset) == 2:
            s = 0
            for i in kset:
                if i == 1:
                    s += 100

                elif i == 5:
                    s += 50

                else:
                    return 0

            return s

        elif len(kset) == 3:
            if kset[0] == kset[1] and kset[0] == kset[2]:
                if kset[0] == 1:
                    return 300;
                elif 2 <= kset[0] <= 6:
                    return 100 * kset[0]
            return 0

        elif len(kset) == 4:
            if kset[0] == kset[1] and kset[0] == kset[2] and kset[0] == kset[3]:
                return 1000
            return 0

        elif len(kset) == 5:
            if kset[0] == kset[1] and kset[0] == kset[2] and kset[0] == kset[3] and kset[0] == kset[4]:
                return 2000
            return 0

        elif len(kset) == 6:
            if kset[0] == kset[1] and kset[0] == kset[2] and kset[0] == kset[3] and kset[0] == kset[4] and kset[0] == kset[5]:
                return 3000
            else:
                num_pairs = 0
                num = {}

                for i in range(1,7):
                    c = kset.count(i)
                    num[i] = c
                    if c == 2:
                        num_pairs += 1

                ## Three Pairs
                if num_pairs == 3:
                    return 1500

                ## Straight
                if num.values().count(1) == 6:
                    return 3000

                return 0

        return 0;


class ParklePlayer(object):
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

        Return: None
        """
        pass

    def decide(self, dice):
        """Append kept-set to kept, return 1 to continue with turn, 0 to stop.
        
        Do NOT:
            Change any scores or roll counts
            Call any methods of a Parkle instance
        
        Return: int
        """
        pass


class ParkleConsoleView(ParkleView):
    pass


class ParkleRealPlayer(ParklePlayer):
    def begin_turn(self):
        pass

    def decide(self, dice):
        pass

