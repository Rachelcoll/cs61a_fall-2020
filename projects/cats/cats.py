"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    true_paras = []
    for paragraph in paragraphs:
        if select(paragraph):
                true_paras.append(paragraph)
    if len(true_paras) <= k:
        return ''
    else:
        return true_paras[k]
    # END PROBLEM 1

from utils import remove_punctuation, split, lower
def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def keyword(n):
        sn = lower(n)
        sn_without_punc = remove_punctuation(sn)
        words = split(sn_without_punc)
        for word in words:
            if word in topic:
                boo = True
                break
            else:
                boo = False
        return boo
    return keyword
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if len(typed_words) == 0:
        return 0.0
    else:
        correct = 0
        for i in range(min(len(typed_words),len(reference_words))):
            if typed_words[i] == reference_words[i]:
                correct += 1
        return (correct / len(typed_words)) * 100.0
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    min = elapsed / 60
    words_typed = len(typed) / 5
    return words_typed / min
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    else:
        low_diffs = 0
        for word in valid_words:
            if diff_function(user_word, word, limit) < limit:
                limit = diff_function(user_word, word, limit)
                low_diffs = word
        if low_diffs == 0:
            return user_word
        return low_diffs
    # END PROBLEM 5



def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    # assert False, 'Remove this line'
    def in_same_len(start, goal):
        if start == goal:
            return 0
        if limit == 0:
            return 1
        if len(start)== 1:
            if start != goal:
                return 1
            else:
                return 0
        else:
            if start[-1] != goal[-1]:
                return 1 + shifty_shifts(start[:-1], goal[:-1], limit-1)
            else:
                return shifty_shifts(start[:-1], goal[:-1], limit)
    if len(start) == len(goal):
        fin_limit = in_same_len(start, goal)
        return fin_limit
    if len(start) != len(goal):
        len_min = min(len(start), len(goal))
        diff = abs(len(start) - len(goal))
        start, goal = start[:len_min], goal[:len_min]
        return in_same_len(start, goal) + diff
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    #assert False, 'Remove this line'

    if limit < 0: # Fill in the condition
        return 314159265358979
    if len(start) == 0 or len(goal) == 0:
        return abs(len(start) - len(goal))
    if start[0] == goal[0]:
        return pawssible_patches(start[1:], goal[1:], limit)
    else:
        add_diff = 1 + pawssible_patches(start, goal[1:], limit-1)
        remove_diff = 1 + pawssible_patches(start[1:], goal, limit-1)
        substitute_diff = 1 + pawssible_patches(start[1:], goal[1:], limit-1)
        return min(add_diff, remove_diff, substitute_diff)
big_limit = 10


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    if limit < 0: # Fill in the condition
        return 314159265358979
    if len(start) == 0 or len(goal) == 0:
        return abs(len(start) - len(goal))
    if start[0] == goal[0]:
        return final_diff(start[1:], goal[1:], limit)
    if len(start) > 1 and len(goal) > 1 and start[0] == goal[1] and start[1] == goal[0]:
        return 1 + final_diff(start[2:], goal[2:], limit-1)
    if len(start) > 1 and len(goal) > 1 and goal[0] == goal[1] and start[0] == goal[0] and start[1] != start[0]:
        return 1 + final_diff(start[1:], goal[2:], limit-1)
    else:
        add_diff = 1 + final_diff(start, goal[1:], limit-1)
        remove_diff = 1 + final_diff(start[1:], goal, limit-1)
        substitute_diff = 1 + final_diff(start[1:], goal[1:], limit-1)
        return min(add_diff, remove_diff, substitute_diff)


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    correct_word = []
    for i in range(len(typed)):
        if typed[i] == prompt[i]:
            correct_word.append(typed[i])
        else:
            break
    progress = len(correct_word) / len(prompt)
    send({'id': user_id, 'progress': progress})
    return progress
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report

def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]

def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    times = []
    for lst in times_per_player:
        time = []
        for i in range(len(lst)-1):
            time.append(lst[i+1]-lst[i])
        times.append(time)
    return game(words, times)
    # END PROBLEM 9



def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    list_lsts = []
    for i in player_indices:
        list_lsts.append([])
    for word_index in word_indices:
        min_time = 114514
        player_min = '玩原神玩的'
        for player_index in player_indices:
            if time(game, player_index, word_index) < min_time:
                player_min = player_index
                min_time = time(game, player_index, word_index)
        list_lsts[player_min].append(word_at(game, word_index))
    return list_lsts
    # END PROBLEM 10




enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)