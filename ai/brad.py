import parkle

class Brad(parkle.ParklePlayer):
    def __init__(self):
        self.name = "Brad"
        self.base_threshold = 0.5  # How "risky" to be for the entire game
        self.turn_threshold = 0.5  # How "risky" to be for current turn

    def begin_turn(self, all_scores, round_score):
        self.score = all_scores[self.n]
        
        avg_diff = 0.0
        
        for i in range(0, len(all_scores)):
            if i == self.n:
                continue
            avg_diff += self.score - all_scores[i]

        avg_diff /= len(all_scores) - 1

        risky_mod = 1
        if avg_diff != 0:
            risky_mod += (avg_diff / 10000.0)
            
        self.turn_threshold = self.base_threshold * risky_mod

    def end_turn(self, all_scores, round_score):
        pass

    def decide(self, odice, all_scores, round_score):

        self.turn_threshold += .05

        group = []
        kset = []
        group.append(kset)

        dice_count = len(parkle.flatten_dice(odice))
        kept_count = 0

        dice = parkle.copy_dice(odice)

        ## Determine if there is a "high scoring" set
        if dice_count == 6:
            if len(dice) == 1:
                kept_count = 6

                for i in range(6):
                    kset.append(dice[0][0])
                    dice[0][1] -= 1

                kset = []
                group.append(kset)

            if len(dice) == 3:
                if dice[0][1] == 2 and dice[1][1] == 2 and dice[2][1] == 2:
                    for i in range(2):
                        kset.append(dice[0][0])
                        dice[0][1] -= 1
                    for i in range(2):
                        kset.append(dice[1][0])
                        dice[1][1] -= 1
                    for i in range(2):
                        kset.append(dice[2][0])
                        dice[2][1] -= 1

                    kept_count = 6
                    kset = []
                    group.append(kset)

            elif len(dice) == 2:
                if dice[0][1] == 3 and dice[1][1] == 3:
                    for i in range(3):
                        kset.append(dice[0][0])
                        dice[0][1] -= 1
                    for i in range(3):
                        kset.append(dice[1][0])
                        dice[1][1] -= 1

                    kept_count = 6

                    kset = []
                    group.append(kset)

            elif len(dice) == 6:
                kept_count = 6

                kset.extend([1, 2, 3, 4, 5, 6])
                kset = []
                group.append(kset)

        ## Take the highest of what's left
        triple_two = -1
        if kept_count == 0:
            m = 0
            for i in range(1, len(odice)):
                if dice[i][1] >= dice[m][1]:
                    if dice[i][0] == 2 and dice[i][1] == 3:
                        triple_two = i
                    else:
                        m = i

            if dice[m][1] >= 3:
                kept_count = dice[m][1]
                for i in range(dice[m][1]):
                    kset.append(dice[m][0])
                    dice[m][1] -= 1
                    kept_count += 1

            else:
                if dice[0][0] == 1:
                    kset.append(1)
                    kset = []
                    group.append(kset)
                    kept_count += 1
                    dice[0][1] -= 1

                elif dice[-1][0] == 5:
                    kset.append(5)
                    kset = []
                    group.append(kset)
                    kept_count += 1
                    dice[-1][1] -= 1

                elif len(dice) > 1 and dice[-2][0] == 5:
                    kset.append(5)
                    kset = []
                    group.append(kset)
                    kept_count += 1
                    dice[-2][1] -= 1

                elif tripe_two >= 0:
                    kset.extend([2, 2, 2])
                    kset = []
                    group.append(kset)
                    kept_count += 3
                    triple_two = -1


        ## Determine if continuing
        if kset == []:
            group = group[:-1]

        self.kept.append(group)

        groupscore = 0
        for i in range(len(group)):
            groupscore += parkle.calculate_set(group[i])

        # passed goal
        res = 0
        if self.score + round_score + groupscore > 10000:
            res = 0

        elif dice_count == 6:
            res = 1

        elif dice_count - kept_count >= 3:
            if dice_count - kept_count == 3 and self.turn_threshold > .75:
                res = 0

            res = 1

        else:
            if self.turn_threshold <= .25:
                res = 1
            else:
                ## get everything else
                res = 0
                if triple_two > 0:
                    group.append([2, 2, 2])
                    kept_count += 3

                if dice[0][0] == 1:
                    for i in range(dice[0][1]):
                        group.append([dice[0][0]])
                        kept_count += 1

                if dice[-1][0] == 5:
                    kset = []
                    for i in range(dice[-1][1]):
                        group.append([dice[-1][0]])
                        kept_count += 1

                if len(dice) > 1 and dice[-2][0] == 5:
                    kset = []
                    for i in range(dice[-2][1]):
                        group.append([dice[-2][0]])
                        kept_count += 1

        #for i in range(len(group)):
        #    print group[i],
        #print
        return res

