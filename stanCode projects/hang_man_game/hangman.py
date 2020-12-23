"""
File: hangman.py
-----------------------------
This program plays hangman game.
Users sees a dashed word, trying to
correctly figure the un-dashed word out
by inputting one character each round.
If the user input is correct, show the
updated word on console. Players have N_TURNS
chances to try and win this game.
"""


import random


# This constant controls the number of guess the player has.
N_TURNS = 7


def main():
    """
    This program will conduct the hangman game. user has N_TURNS to guess the character within ans to un-dashed word.
    """

    ans = random_word()
    hint = s_hint(ans)
    chance = N_TURNS
    while True:
        # user lose and the program will stop and reveal answer if user run out of chance
        if chance == 0:
            print('Your are completely hung : (')
            print('The word was ' + ans)
            break
        else:
            # continue to guess if user hasn't found out the ultimate answer
            if hint != ans:
                print('The word looks like:' + hint)
                print('You have ' + str(chance) + ' guess left.')
                guess = input('Your guess: ')
                # check if user's input is a valid input
                guess = check_format(guess)
                # show correct message if the valid input is within "ans"
                if ans.find(guess) > -1:
                    hint = correct_guess(ans, guess, hint)
                # remind user it's wrong and deduct chance number by 1
                else:
                    chance -= 1
                    print('There\'s no ' + guess + ' in the word.')
            # print win message when user find out all characters within "ans"
            else:
                print('You Win!')
                print('The word was: ' + ans)
                break


def correct_guess(ans, guess, hint):
    """
    :param ans: str, the word to be guessed, generate by random selection
    :param guess: str, input from the user to guess character within "ans"
    :param hint: str, dashed version of "ans" to show number of character within this word as a hint for user
    :return: str, updated hint with character and its position within "ans" in upper class
    """
    new_hint = ''
    for i in range(len(hint)):
        ch_ans = ans[i]
        ch_hint = hint[i]
        # add guess to the same position of ans within hint
        if guess == ch_ans:
            new_hint += ch_ans
        # the rest position stay as it
        else:
            if ch_hint == '-':
                new_hint += '-'
            else:
                new_hint += ch_hint
    hint = new_hint
    print('You are correct!')
    return hint


def check_format(guess):
    """
    :param guess: str, input from the user to guess character within "ans"
    :return: str, upper class of alphabet character entered by user
    """
    while True:
        guess = guess.upper()
        ans_format = guess.isalpha()
        if ans_format is True:
            if len(guess) == 1:
                return guess
                break
            else:
                print('Illegal format')
                guess = input('Your guess: ')
        else:
            print('Illegal format')
            guess = input('Your guess: ')


def s_hint(ans):
    """
    :param ans: str, the answer for user to guess
    :return: str, dashed version of "ans" to show number of character within this word as a hint for user
    """
    hint = ''
    for i in range(len(ans)):
        hint += '-'
    return hint


def random_word():
    num = random.choice(range(9))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"


#####  DO NOT EDIT THE CODE BELOW THIS LINE  #####
if __name__ == '__main__':
    main()
