## Parkle
## Zolmeister

import parkle

class zolmeister(parkle.ParklePlayer):
  def __init__(self):
    self.name = "Zolmeister"#raw_input("Bot Name: ")
    print
    
  def begin_turn(self, all_scores, round_score):
    self.score = all_scores[self.n]
  
  def decide(self, dice, all_scores, round_score):
    from random import randint
    from itertools import combinations
    
    riskTolerance = 1600
    currentScore = self.score
    def flatten_dice(dice):
      nd = []
      for value in dice:
          for i in range(value[1]):
              nd.append(value[0])
  
      return nd
  
    def nest_dice(flattened_dice):
      dice = []
      for i in range(1, 7):
          c = flattened_dice.count(i)
          if c == 0:
              continue
  
          dice.append([i, c])
          
      return dice
    dice = flatten_dice(dice)

    expected = {
      6: 404.0,
      5: 237.6,
      4: 159.7,
      3: 109.2,
      2: 94.8,
      1: 159.2
    }
    
    fail = {
        6: 0.025,
        5: 0.078,
        4: 0.158,
        3: 0.279,
        2: 0.447,
        1: 0.676
    }
    
    def botMove(dice):
      # first decide how many dice you can take based on risk
      risk = {}
      
      for key in xrange(1, len(dice)+1):
        risk[key] = expected[key] - fail[key] * currentScore
      
      canTake = []
      valid = validFor(dice, len(dice))
      #print"valid moves", valid
      for key in risk:
        # check if its valid for me to keep how many I want to
        if risk[key] >= 0 and key in valid:
          canTake.append(key)
            
          
      #print"can take", canTake
      
      # get all possible combinations of what I can keep for the number of dice that I can take
      allPossible = []
      for d in canTake:
        allPossible+=list(combinations(dice, d))
      
      # for each possiblity, calculate its expected value
      
      bestScore = 0
      diceUsed = []
      for combination in allPossible:
        left = len(dice) - len(combination)
        if left == 0:
          left = 6
          
        # CurrentScore = (expected - risk tolerance) / failure
        bonus = (expected[left] - riskTolerance) / fail[left]
        score = maxScore(combination) + bonus
        
        if score > bestScore or score == bestScore and len(combination) < len(diceUsed):
          bestScore = score
          diceUsed = combination
      
      if bestScore == 0:
        # if I can't take anything, return the best valid move and stop
        #print"cant take anything, returning best valid move"
        bestScore = 0
        diceUsed = []
        for n in xrange(1, len(dice) + 1):
          for combo in combinations(dice, n):
            score = maxScore(list(combo))
            if score > bestScore or score == bestScore and len(combo) < len(diceUsed):
              bestScore = score
              diceUsed = combo
              #print "new best score", score, "with", combo
        
        # a manual override for rolling all the dice again, regardless of risk
        again = False
        if len(diceUsed) == len(dice):
          again = True
        return (diceUsed, again)
      
      # returns ( [dice kept], True/False - reroll )
      return (diceUsed, True)
    
    def roll(n):
      return [randint(1, 6) for x in xrange(n)]
    
    def maxScore(dice):
      if not dice:
        return 0
      
      # six of a kind - 3000
      if dice.count(dice[0]) == 6:
        #print"six of a kind"
        return 3000
      
      # two triplets - 2500
      if len(dice) == 6:
        if len(set(dice)) == 2 and dice.count(list(set(dice))[0]) == 3:
          #print"two triplets"
          return 2500
      
      # 5 of a kind - 2000
      for d in set(dice):
        if dice.count(d) == 5:
          return maxScore(filter(lambda x: x != d, dice)) + 2000
      
      # straight - 1500
      if len(set(dice)) == 6:
        #print"straight"
        return 1500
      
      # three pairs - 1500
      if len(dice) == 6:
        threePairs = True
        for d in set(dice):
          if dice.count(d) != 2:
            threePairs = False
        if threePairs:
          #print"three pairs"
          return 1500
      
      # 4 of a kind - 1000
      for d in set(dice):
        if dice.count(d) == 4:
          #print"4 of a kind"
          return maxScore(filter(lambda x: x != d, dice)) + 1000
      
      # 3x
        # 6 - 600
        # 5 - 500
        # 4 - 400
        # 3 - 300
        # 2 - 200
        
      for d in set(dice):
        if d != 1 and dice.count(d) == 3:
          return maxScore(filter(lambda x: x != d, dice)) + d * 100
        
      # 1 - 100
      if 1 in set(dice):
        return maxScore(filter(lambda x: x != 1, dice)) + dice.count(1) * 100
      
      # 5 - 50
      if 5 in set(dice):
        return maxScore(filter(lambda x: x != 5, dice)) + dice.count(5) * 50
      
      return 0
    
    def validFor(dice, n=None):
      if n == None:
        n = len(dice)
        
      if not dice or n == 0:
        return []
      
      # six of a kind - 3000
      if dice.count(dice[0]) == 6 and n == 6:
        return [6] + validFor(dice, n-1)
      
      # two triplets - 2500
      if len(dice) == 6:
        if len(set(dice)) == 2 and dice.count(list(set(dice))[0]) == 3 and n == 6:
          return [6] + validFor(dice, n-1)
      
      # 5 of a kind - 2000
      for d in set(dice):
        if dice.count(d) >= 5 and n == 5:
          return [5] + validFor(dice, n-1) + map(lambda x: x + 5, validFor(filter(lambda x: x != d, dice)))
      
      # straight - 1500
      if len(set(dice)) == 6 and n == 6:
        return [6] + validFor(dice, n-1)
      
      # three pairs - 1500
      if len(dice) == 6:
        threePairs = True
        for d in set(dice):
          if dice.count(d) != 2:
            threePairs = False
        if threePairs and n == 6:
          return [6] + validFor(dice, n-1)
      
      # 4 of a kind - 1000
      for d in set(dice):
        if dice.count(d) >= 4 and n == 4:
          return [4] + validFor(dice, n-1) + map(lambda x: x + 4, validFor(filter(lambda x: x != d, dice)))
      
      # 3x
        # 6 - 600
        # 5 - 500
        # 4 - 400
        # 3 - 300
        # 2 - 200
        
      for d in set(dice):
        if dice.count(d) >= 3 and n == 3:
          return [3] + validFor(dice, n-1) + map(lambda x: x + 3, validFor(filter(lambda x: x != d, dice)))
        
      if n == 2:
        if dice.count(1) + dice.count(5) > 1:
          return [2] + validFor(dice, n-1)
        
      if n == 1:
        if dice.count(1) + dice.count(5) > 0:
          return [1]
    
      return validFor(dice, n-1)
    
    kept, cont = botMove(dice)
    
    def grouper(dice):
      if not dice:
        return []
      
      # six of a kind - 3000
      if dice.count(dice[0]) == 6:
        #print"six of a kind"
        return [dice]
      
      # two triplets - 2500
      if len(dice) == 6:
        if len(set(dice)) == 2 and dice.count(list(set(dice))[0]) == 3:
          #print"two triplets"
          return [dice]
      
      # 5 of a kind - 2000
      for d in set(dice):
        if dice.count(d) == 5:
          return [grouper(filter(lambda x: x != d, dice)), [d for x in xrange(5)]]
      
      # straight - 1500
      if len(set(dice)) == 6:
        #print"straight"
        return [dice]
      
      # three pairs - 1500
      if len(dice) == 6:
        threePairs = True
        for d in set(dice):
          if dice.count(d) != 2:
            threePairs = False
        if threePairs:
          #print"three pairs"
          return [dice]
      
      # 4 of a kind - 1000
      for d in set(dice):
        if dice.count(d) == 4:
          #print"4 of a kind"
          return [grouper(filter(lambda x: x != d, dice)),[d for x in xrange(4)]]
      
      # 3x
        # 6 - 600
        # 5 - 500
        # 4 - 400
        # 3 - 300
        # 2 - 200
        
      for d in set(dice):
        if d != 1 and dice.count(d) == 3:
          return [grouper(filter(lambda x: x != d, dice)) , [d for x in xrange(3)]]
        
      # 1 - 100
      if 1 in set(dice):
        return [grouper(filter(lambda x: x != 1, dice)) , [[1] for x in xrange(dice.count(1))]]
      
      # 5 - 50
      if 5 in set(dice):
        return [grouper(filter(lambda x: x != 5, dice)) , [[5] for x in xrange(dice.count(5))]]
      
      return []
    
    group = []
    def mapper(lst):
      for l in lst:
        try:
          assert isinstance(l[0], (list, tuple))
          mapper(l)
        except:
          group.append(l)
        
    mapper(grouper(kept))
    group = filter(lambda x: len(x) > 0, group)
    
    
    self.kept.append(group)
    if cont:
      return 1
    return 0