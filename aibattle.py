
import sys
import os

import parkle

class ParkleAIBattleView(parkle.ParkleView):
    def start_game(self):
        print "Parkle v0.3.0\n----------------\n"

        players = []
        while(1):
            print "Add Player (currently have {0}):".format(len(players))
            if len(players) < 2:
                print "\t(a)i player\n\t(q)it\n"

            else:
                print "\t(a)i player\n\t(s)tart game\n\t(q)uit\n"

            r = raw_input(":")

            if r.lower() == "q":
                return

            elif r.lower() == "s":
                if len(players) >= 2:
                    break
                print "You must have at least two players to start."
                continue

            elif r.lower() == "a":
                path = raw_input("File path: ")
                #class_name = raw_input("Class Name: ")
                sys.path.append('ai')
                try:
                    namespace = {}
                    m = __import__(path)
                    p = m.__dict__[path]()
                    players.append(p)

                except ImportError, AttributeError:
                    print "Couldn't find file/class.\n"
                continue

            else:
                continue

        self.rounds = int(raw_input("Number of rounds: "))
        self.rounds_played = 0
        if self.rounds < 40:
            self.dot_every = 1
        else:
            self.dot_every = self.rounds / 40


        matches_won = []
        for pl in players:
            matches_won.append(0)

        for i in range(self.rounds):
            self.begin_game(players)
            self.rounds_played += 1

            i = 0
            for p in self.game.players:
                if p == self.winning_player:
                    matches_won[i] += 1

                i += 1

        print "\n"
        for p in self.game.players:
            print "  {0}: {1}".format(p.name, matches_won[p.n])


if __name__ == "__main__":
    v = ParkleAIBattleView()
    v.start_game()

