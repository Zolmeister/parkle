## Parkle
## Zoli Kahan

import parkle

class zoli(parkle.ParklePlayer):
    def __init__(self):
        self.name = "Zoli"#raw_input("Bot Name: ")
        print
    
    def decide(self, dice, all_scores, round_score):
        def rerollable(diceR):
            for i in diceR:
                if i[0]==5 or i[0]==1:
                    return len(parkle.flatten_dice(diceR))-1
            return 0
        def rerollK(diceK):
            for i in range(len(diceK)):
                if diceK[i][0]==1:
                    return [1]
                elif diceK[i][0]==5:
                    return [5]
                
            return diceK
        #print round_score
        def getMax(diceM):
            keptset2 = []
            if parkle.calculate_set(diceM)>0:
                return parkle.flatten_dice(diceM)
            for i in range(len(diceM)):
                if diceM[i][1]>=3:
                    for n in range(diceM[i][1]):
                        keptset2.append(diceM[i][0])
            return keptset2

        
        keptset = []
        d = parkle.copy_dice(dice)
        m=getMax(dice)
        #print m
        #print calculate_set(m)
        #print calculate_set(m)>=400
        if parkle.calculate_set(m)+round_score>=400 and len(m)<6:
            self.kept.append([m])
        elif parkle.calculate_set(m)+round_score>=400:
            self.kept.append([m])
            return 1
        elif rerollable(dice)>=3:
            self.kept.append([rerollK(dice)])
            #print(rerollK(dice))
            return 1
        else:
            self.kept.append([[]])
        #print self.kept


            
        """if d[0][0] == 1 and d[0][1] >= 1:
            l = d[0][1]
            if l == 2:
                self.kept.append([[1], [1]])
            else:
                for j in range(l):
                    keptset.append(1)
                    d[0][1] -= 1

                self.kept.append([keptset])

        else:
            self.kept.append([[]])
        """
        return 0
