"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.
FIRST_101_DIGITS_OF_PI = 31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided): #返回一轮骰子总点数或1
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    dtotal = 0
    pigout = False
    for i in range (num_rolls):
        onedice = dice()
        dtotal += onedice
        if onedice == 1:
            pigout = True
    if pigout == True:
        return 1
    else:
        return dtotal
# print(roll_dice(9,make_test_dice(6)))
    # END PROBLEM 1


def free_bacon(score):#n为对面分数，k为对面分数n对应的pi小数点后第n位的值
    #返回玩家不投色子可以获得的分数
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    pi = FIRST_101_DIGITS_OF_PI

    # Trim pi to only (score + 1) digit(s)
    # BEGIN PROBLEM 2
    inverse_score = 100 - score
    k = 0
    while k < inverse_score:
        pi, k = pi//10, k+1
        #score: 1 total:101 left:2 trim: 99times
    # END PROBLEM 2

    return pi % 10 + 3
# print(free_bacon(2))


def take_turn(num_rolls, opponent_score, dice=six_sided):
    #返回单个玩家一轮的最终得分
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3
# print(take_turn(3, 0, make_test_dice(1,2,3)))


def extra_turn(player_score, opponent_score):
    """Return whether the player gets an extra turn."""
    return (pig_pass(player_score, opponent_score) or
            swine_align(player_score, opponent_score))


def swine_align(player_score, opponent_score):
    #当前玩家投完骰子，若两人分数不为0且最大公约数不小于10，当前玩家可以再扔一次
    """Return whether the player gets an extra turn due to Swine Align.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> swine_align(30, 45)  # The GCD is 15.
    True
    >>> swine_align(35, 45)  # The GCD is 5.
    False
    """
    # BEGIN PROBLEM 4a
    GCD = 0
    k = 1
    if player_score == 0 or opponent_score == 0:
        return False
    else:
        a = min(player_score, opponent_score)
        b = max(player_score, opponent_score)
        while k <= a:
            if a % k == 0 and b % k == 0:
                GCD = k
            k += 1
        if GCD >= 10:
            return True
        else:
            return False
# print(swine_align(11,22))
    # END PROBLEM 4a

def pig_pass(player_score, opponent_score):
    #如果当前玩家分数比对方玩家低3分以内，可以再扔一次骰子
    """Return whether the player gets an extra turn due to Pig Pass.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> pig_pass(9, 12)
    False
    >>> pig_pass(10, 12)
    True
    >>> pig_pass(11, 12)
    True
    >>> pig_pass(12, 12)
    False
    >>> pig_pass(13, 12)
    False
    """
    # BEGIN PROBLEM 4b
    if opponent_score - player_score > 0 and opponent_score - player_score <3:
        return True
    else:
        return False


def other(who):#返回当前另一个玩家的代号数值 who:当前玩家代号
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided, goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn. strategy决定每轮player能扔几个骰子

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    #思路，在各玩家点数不大于目标前提下轮流掷色子，每次轮到一个玩家需要考虑额外轮的情况以及播报话语，引入strategy函数帮助确定每次掷骰子要扔几个
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    say = say(score0,score1)
    while score0 < goal and score1 < goal:
        if who == 0:
            dice_num = strategy0(score0, score1)
            score0 += take_turn(dice_num, score1, dice)
            say = say(score0, score1)
            if extra_turn is False:
                who = other(who)
        if who == 1:
            dice_num = strategy1(score1, score0)
            score1 += take_turn(dice_num, score0, dice)
            say = say(score0, score1)
            if extra_turn is False:
                who = other(who)

    return score0, score1

'''below are better solution for problem 5'''
    # while score0 < goal and score1 < goal:
    #     if who == 0: 
    #         num_of_dice = strategy0(score0, score1)
    #         score0 += take_turn(num_of_dice, score1, dice)
    #         say = say(score0, score1)
    #         if not extra_turn(score0, score1): # Only change who if there is no extra turn
    #             who = other(who)
       
    #     elif who == 1:
    #         num_of_dice = strategy1(score1, score0)
    #         score1 += take_turn(num_of_dice, score0, dice)
    #         say = say(score0, score1)
    #         if not extra_turn(score1, score0): # Only change who if there is no extra turn
    #             who = other(who)
    # END PROBLEM 5

    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 6
    # END PROBLEM 6


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 8)
    Player 0 now has 10 and Player 1 now has 8
    >>> h3 = h2(10, 17)
    Player 0 now has 10 and Player 1 now has 17
    Player 1 takes the lead by 7
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, last_score=0, running_high=0):
    assert who == 0 or who == 1, "The who argument should indicate a player."
#last_score是该玩家在这一轮之前的积分，running_high是该玩家之前单轮最高获得积分
#返回一个可以输入01玩家成绩并输出评论该玩家下一轮成绩的函数，同时可以打印对当前玩家该轮成绩的评论
    # BEGIN PROBLEM 7
    def say(score0,score1):
        # if who == 0:
        #     gain = score0 - last_score
        #     if gain > running_high:
        #         print(gain, "point(s)! The most yet for Player", who)
        #         running_high = gain
        #     return announce_highest(0, score0, running_high)
        # if who == 1:
        #     gain = score1 - last_score
        #     if gain > running_high:
        #         print(gain, "point(s)! The most yet for Player", who)
        #         running_high = gain
        #     return announce_highest(1, score1, running_high)
        if who == 0:
            score = score0
        if who == 1:
            score = score1
        gain = score - last_score
        if gain > running_high:
            print(gain, "point(s)! The most yet for Player", who)
            running_high = gain
        return announce_highest(who, score, running_high)

    return say


    # END PROBLEM 7

#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.
    #stategy函数接受当前玩家和对手的成绩，返回当前玩家应当投的骰子数
    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, trials_count=1000):
    #输入一个函数和指定执行次数，返回一个函数，向该返回函数输入原始函数的要求参数可以返回该函数执行参数指定执行次数得到的平均值
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def average(*arg):
        sum = 0
        for i in range(trials_count):
            sum += original_function(*arg)
        return sum/trials_count
    return average
    # END PROBLEM 8

def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    #输入骰子方式和投掷总数，使用make_averaged函数计算投掷投掷总数次时每次不同骰子投掷数得到的成绩平均值，返回最适单次投掷数
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    max_times = 0
    max_average = 0
    for i in range(1,11):
        f = make_averaged(roll_dice, trials_count)
        average = f(i, dice)
        if average > max_average:
            max_average = average
            max_times = i

    return max_times
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test extra_turn_strategy
        print('extra_turn_strategy win rate:', average_win_rate(extra_turn_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

'''def free_bacon(score):#n为对面分数，k为对面分数n对应的pi小数点后第n位的值
    #返回玩家不投色子可以获得的分数'''


def bacon_strategy(score, opponent_score, cutoff=910, num_rolls=max_scoring_num_rolls()):
    """This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if free_bacon(opponent_score) >= cutoff:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10
# print(free_bacon(36))


def extra_turn_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers an extra turn. It also
    rolls 0 dice if it gives at least CUTOFF points and does not give an extra turn.
    Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    free_bacon_plus = free_bacon(opponent_score)
    score += free_bacon_plus
    if free_bacon_plus >= cutoff or swine_align(score, opponent_score) or pig_pass(score, opponent_score):
        return 0
    return num_rolls
    # END PROBLEM 11


# def fix_cutoff(score, opponent_score, num_rolls=max_scoring_num_rolls()):
#     win_rate = 0
#     cutoff = 0
#     for i in range(3,13):
#         def strategy(i):
#             free_bacon_plus = free_bacon(opponent_score)
#             score += free_bacon_plus
#             if free_bacon_plus >= i or swine_align(score, opponent_score) or pig_pass(score, opponent_score):
#                 return 0
#             return num_rolls
#         rate = average_win_rate(strategy)
#         if rate > win_rate:
#             rate = win_rate
#             cutoff = i
#     return cutoff
# print(fix_cutoff(0, 19))


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    

run_experiments()
##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()