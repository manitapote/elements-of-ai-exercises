# Automatic Sebastian game player
# B551 Fall 2020
# PUT YOUR NAME AND USER ID HERE!
#
# Andrew Doto: adoto
# Karthikeya Kethamakka: kketham
# Manita Pote: potem
#
# Based on skeleton code by D. Crandall
#
#
# This is the file you should modify to create your new smart player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from SebastianState import Dice
from SebastianState import Scorecard
import random

# This function takes in the dice and the scorecard
# It's modeled after the scorecard record function
# Overall, it takes in the dice and finds the category that will yield the highest score
def max_score(dice, scorecard):
    # counts for each of the possible dice values
    counts = [dice.count(i) for i in range(1,7)]
    # max score output, has the category for recording and 
    # the corresponding score
    max_score = ['category', 0]
    
    # for each category in the game
    for category in Scorecard.Categories:
        # check if the category has been used yet, if so, don't consider
        # then go through each category and check for criteria
        # if the category yields a better score, replace it
        if category in scorecard.scorecard:
            break
        if category in Scorecard.Numbers:
            score = counts[Scorecard.Numbers[category]-1] * Scorecard.Numbers[category]
        elif category == "company":
            score = 40 if sorted(dice) == [1,2,3,4,5] or sorted(dice) == [2,3,4,5,6] else 0
        elif category == "prattle":
            score = 30 if (len(set([1,2,3,4]) - set(dice)) == 0 or len(set([2,3,4,5]) - set(dice)) == 0 or len(set([3,4,5,6]) - set(dice)) == 0) else 0
        elif category == "squadron":
            score = 25 if (2 in counts) and (3 in counts) else 0
        elif category == "triplex":
            score = sum(dice) if max(counts) >= 3 else 0
        elif category == "quadrupla":
            score = sum(dice) if max(counts) >= 4 else 0
        elif category == "quintuplicatam":
            score = 50 if max(counts) == 5 else 0
        elif category == "pandemonium":
            score = sum(dice)
        else:
            print("Error: unknown category")

        if score > max_score[1]:
            max_score = [category, score]
    
    # after the loop, check the max score to see if the dice doesn't qualify for any category
    # this was a judgement call based on experimentation, but I've selected these two 
    # as they are more rare, so I'm "preserving" the higher probability categories for later
    if max_score[0] == 'category':
        if 'quintuplicatam' not in scorecard.scorecard:
            max_score[0] = 'quintuplicatam'
        elif 'quadrupla' not in scorecard.scorecard:
            max_score[0] = 'quadrupla'
        else: 
            max_score[0] = random.choice([c for c in Scorecard.Categories if c not in scorecard.scorecard])
    
    return max_score

# this function takes in dice, strategy in the form of a boolean list, and the scorecard
# then it takes a look at all possibilities of that strategy
# and returns the expected score of that strategy
# This strategy was inspired by the discussion video that Prof Crandall did
def exp_value_reroll(dice, strategy, scorecard):
    total_outcomes = 0
    score = 0
    for outcome_a in ([dice[0],] if strategy[0] == False else range(1,7)):
        for outcome_b in ([dice[1],] if strategy[1] == False else range(1,7)):
            for outcome_c in ([dice[2],] if strategy[2] == False else range(1,7)):
                for outcome_d in ([dice[3],] if strategy[3] == False else range(1,7)):
                    for outcome_e in ([dice[4],] if strategy[4] == False else range(1,7)):
                        total_outcomes +=1
                        new_dice = [outcome_a, outcome_b, outcome_c, outcome_d, outcome_e]
                        score += max_score(new_dice, scorecard)[1]
            
    return score * (1/total_outcomes)

# this function takes in the dice and scorecard
# then it looks at all possibilities of reroll strategy
# then looks at expected values for all reroll strategies and returns the best one
# This strategy was inspired by the discussion video that Prof Crandall did
def find_best_strategy(dice, scorecard):
    best_score = 0 
    best_strategy = []
    for reroll_a in (True, False):
        for reroll_b in (True, False):
            for reroll_c in (True, False):
                for reroll_d in (True, False):
                    for reroll_e in (True, False):
                        strategy = [reroll_a, reroll_b, reroll_c, reroll_d, reroll_e]
                        score = exp_value_reroll(dice, strategy, scorecard)
                        if score > best_score:
                            best_score = score
                            best_strategy = strategy
    return [i for i, x in enumerate(best_strategy) if x == True]

class SebastianAutoPlayer:

    def __init__(self):
            pass  
    
    def first_roll(self, dice, scorecard):
        dice = dice.dice
        return find_best_strategy(dice, scorecard)

    def second_roll(self, dice, scorecard):
        dice = dice.dice
        return find_best_strategy(dice, scorecard)
      
    def third_roll(self, dice, scorecard):
        dice = dice.dice
        return max_score(dice, scorecard)[0]

