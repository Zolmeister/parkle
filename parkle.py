## Parkle 0.2
##
## Bradley Zeis
## Zoli Kahn

import sys
import os

import random
rand = random.Random()

def copy_dice(dice):
   d = []
   for i in dice:
       d.append(list(i))
   return d

def points_possible(dice):
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

def calculate_one_keptset(kset):
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
            num_triples = 0
            num = {}

            for i in range(1,7):
                c = kset.count(i)
                num[i] = c
                if c == 2:
                    num_pairs += 1
                if c == 3:
                    num_triples += 1

            ## Three Pairs
            if num_pairs == 3:
                return 1500

            ## Two Triples
            if num_triples == 2:
                return 1500

            ## Straight
            if num.values().count(1) == 6:
                return 3000

            return 0

    return 0;


class ParkleView(object):
    def __init__(self):
        self.game = None
        self.current_player = None
        self.winning_player = None

    def start_game(self):
        """Setup the player list and the view environmant, if necessary.
        
        Always end this method with a call to begin_game.
        """
        pass

    def begin_game(self, players):
        """Instantiate the game and begin it.
        
        Do not override in subclasses.
        """
        self.game = Parkle(self)
        self.game.players = players
        self.current_player = None
        self.winning_player = None
        self.winning_player = self.game.start_game()
        self.end_game()

    def end_game(self):
        pass

    def start_round(self):
        pass

    def end_round(self):
        pass

    def start_turn(self):
        pass

    def end_turn(self):
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
        self.scores = []
    
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

        self.scores = []
        n = 0
        for p in self.players:
            self.scores.append(0)
            p.n = n
            n += 1
        
        rand.seed()
        while 1:

            self.view.start_round()

            for p in self.players:
                r = self.turn(p)
                if r == -1:
                    return None

            self.view.end_round()

            m = self.goal
            for p in self.players:
                if self.scores[p.n] >= m:
                    m = p

            if m != self.goal:
                return m
                    
    
    def turn(self, player):
        self.view.current_player = player
        self.view.start_turn()
        player.rolls = 0
        player.kept = []
        player.begin_turn()

        res = 0

        dice_left = 6
        round_score = 0
        reroll = True
        lost = False
        while 1:
            if reroll:
                d = self.roll(dice_left);
                player.rolls += 1

            reroll = True

            self.view.roll(copy_dice(d))

            if not points_possible(d):
                player.kept = []
                round_score = 0
                lost = True
                break

            result = player.decide(copy_dice(d), list(self.scores), round_score)
            self.view.decide()

            if result == -1:
                res = -1;
                break

            ## Determine if newest kept-sets are valid
            ## If invalid, remove new sets from kept, start over with same roll
            try:
                group = player.kept[-1]
            except:
                self.view.invalid_decision()
                reroll = False
                continue

            c = 0

            groupscore = 0
            for keptset in group:
                setscore = calculate_one_keptset(keptset)
                c += len(keptset)
                if not setscore:
                    if len(keptset) == 0 and len(player.kept) == 1:
                        lost = True
                        break

                    self.view.invalid_decision()
                    player.kept = player.kept[:-1]
                    reroll = False
                    break

                else:
                    groupscore += setscore

            if lost:
                break

            if not reroll:
                continue

            round_score += groupscore

            if result == 0:
                break

            dice_left -= c
            if dice_left == 0:
                dice_left = 6
            elif dice_left < 0 or dice_left > 6:
                player.kept = []
                s = 0
                break

        if not lost:
            self.scores[player.n] += round_score
        self.view.end_turn(round_score)
        return res



class ParklePlayer(object):
    def __init__(self):
        self.name = ""
        self.kept = []; # [[[1, 1], [5]], [[3, 3, 3]]] = Pair of 2s and a 5 kept first roll, triple 3s kept second roll
                        # Each sublist is called a "kept-set"
        self.n = 0      # Player order
        self.rolls = 0  # Number of rolls this turn

    def begin_turn(self):
        """User-defined setup method for the beginning of a turn.
        
        No altering of kept should be done here, only pre-calculations.

        Return: None
        """
        pass

    def decide(self, dice, all_scores, round_score):
        """Create a group of keptsets, append the group to self.kept.
        
        Do NOT:
            Change any scores or roll counts
            Call any methods of a Parkle instance
        
        Return: int
        """
        pass



class ParkleConsoleView(ParkleView):
    def start_game(self):
        print "Parkle v0.2\n----------------\n"

        players = []
        while(1):
            print "Add Player:"
            if len(players) < 2:
                print "\t(h)uman player\n\t(a)i player\n\t(q)it\n"

            else:
                print "\tAdd (h)uman player\n\t(a)i player\n\t(s)tart game\n\t(q)uit\n"

            r = raw_input(":")

            if r.lower() == "q":
                return

            elif r.lower() == "s":
                if len(players) >= 2:
                    break
                print "You must have at least two players to start."
                continue

            elif r.lower() == "h":
                p = ParkleRealPlayer()
                p.name = raw_input("Player Name: ")
                players.append(p)
                continue

            elif r.lower() == "a":
                path = raw_input("File path: ")
                class_name = raw_input("Class Name: ")
                sys.path.append(os.path.split(path)[0])
                module = __import__(os.path.split(path)[1][:-3])
                c = module.__dict__[class_name]
                p = c()
                players.append(p)
                continue

            else:
                continue

        self.begin_game(players)

    def end_game(self):
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"


        for p in self.game.players:
            if p == self.winning_player:
                print "* {0}: {1}".format(p.name, self.game.scores[p.n])
            else:
                print "  {0}: {1}".format(p.name, self.game.scores[p.n])

        print "\n(r)eplay, (n)ew game"

        r = raw_input(":")
        if r.lower() == "r":
            self.begin_game(self.game.players)

        if r.lower() == "n":
            self.start_game()


    def start_round(self):
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        for p in self.game.players:
            print "{0}: {1}".format(p.name, self.game.scores[p.n])

        print

    def start_turn(self):
        print "--------------------------------------------------------------------------------"
        print "{0}'s turn.\n\tScore: {1}".format(self.current_player.name, self.game.scores[self.current_player.n])

    def end_turn(self, round_score):
        print "\nRound Score: {0}\nTotal Score: {1}\n".format(round_score, self.game.scores[self.current_player.n])

    def roll(self, dice):
        print "Roll {0}:\n\t".format(self.current_player.rolls),
        for i in dice:
            for j in range(i[1]):
                print i[0],
        print

    def invalid_decision(self):
        print "Decision invalid, please select something else."


class ParkleRealPlayer(ParklePlayer):
    def begin_turn(self):
        pass

    def decide(self, dice, all_scores, round_score):
        d = copy_dice(dice)
        group = []      ## Group of keptsets from this roll
        keptset = []
        group.append(keptset)
        first = True
        while 1:

            if not first:
                print "\t",
                for i in d:
                    for j in range(i[1]):
                        print i[0],

                print

            first = False

            for i in self.kept:
                for j in i:
                    print j,

            if len(self.kept):
                print "|",

            for k in group:
                print k,
            
            print "\n(Round Score: {0})".format(round_score)

            print "\nWhat would you like to keep?"
            k = raw_input(":")

            if k == "c":
                for i in range(len(group)):
                    if len(group[i]) == 0:
                        group = []
                        keptset = []
                        group.append(keptset)

                self.kept.append(group)
                print "----------------\n"
                return 1

            elif k == "s":
                if not len(keptset):
                    group = group[:-1]
                self.kept.append(group)
                return 0

            elif k == "n":
                keptset = []
                group.append(keptset)
                continue

            elif k == "a":
                for i in d:
                    for j in range(i[1]):
                        keptset.append(i[0])


            elif k == "l":
                return -1

            elif k == "p":
                d = copy_dice(dice)
                group = []
                keptset = []
                group.append(keptset)
                continue
            
            else:
                try:
                    i = int(k)
                except:
                    continue

                for j in d:
                    if j[0] == i and j[1] >= 1:
                        j[1] -= 1
                        keptset.append(i)
                        break


class JimmyBot(ParklePlayer):

    """This bot is a proof of concept to test if AI bots work.
    
    It is not meant to be a real opponent for either humans or
    other bots.
    
    
    Note: JimmyBot will get caught in an infinite loop if there are no
    ones in his first roll.
    """

    def __init__(self):
        self.name = "Jimmy Bot"


    def decide(self, dice, all_scores, round_score):
        keptset = []
        d = copy_dice(dice)
        if d[0][0] == 1 and d[0][1] >= 1:
            l = d[0][1]
            for j in range(l):
                keptset.append(1)
                d[0][1] -= 1

            self.kept.append([keptset])

        else:
            self.kept.append([[]])

        return 0
         

