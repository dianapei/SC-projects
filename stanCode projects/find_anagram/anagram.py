"""
File: anagram.py
Name: Diana Pei-Rung Yu
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop

# Global variable
dictionary = {}               # to save all the words in FILE


def main():
    """
    This program will find the anagrams of the word provide by user.
    user can leave the program by enter EXIT constant
    """
    print('Welcome to stanCode \"Anagram Generator\" (or -1 to quit)')
    read_dictionary()
    while True:
        # get word from user
        word = input('Find anagram for: ')
        # to be case insensitive
        word = word.lower()
        if word == EXIT:
            break
        else:
            find_anagrams(word)


def read_dictionary():
    """
    this function add all the words in FILE to global variable dictionary by use the alphabet letter as keys
    and words come with the alphabet as values
    """
    global dictionary
    with open(FILE, 'r') as f:
        for line in f:
            # clear the front and behind each line to have clean word
            line = line.strip()
            # add word to dictionary
            if line[0] not in dictionary:
                dictionary[line[0]] = [line]
            else:
                dictionary[line[0]].append(line)


def find_anagrams(s):
    """
    :param s: the word provide by user
    :return: the anagram in dictionary
    """
    # tell user the program is searching for anagram
    print('Searching...')
    # to store the anagrams that can be found in dictionary
    a_lst = []
    # turn the string given by user into lst
    s_lst = word_generator(s)
    # use s_lst to get character combinations and see if it's in dictionary
    find_anagrams_helper(s_lst, len(s_lst), [], a_lst)
    # show the number of anagrams we found and list of the anagrams
    print(len(a_lst), 'anagrams: ', a_lst)


def word_generator(s):
    """
    :param s: str, the the word get from user
    :return: lst, list contain all characters within s
    """
    s_lst = []
    for i in range(len(s)):
        ch = s[i]
        s_lst.append(ch)
    return s_lst


def find_anagrams_helper(lst, target, current, a_lst):
    """
    :param lst: lst, contain all the characters
    :param target: num, target length of current which is same as the length of the word provide by user
    :param current: lst, to store the characters by order
    :param a_lst: lst, to store the anagram of the word provided by user
    :return: lst, all anagram words
    """
    # check word if current length equals to lst
    if len(current) == target:
        # turn the current character order list into string
        candidate = word_processor(current)
        # avoid to have duplicate anagram
        if candidate in a_lst:
            return
        else:
            # check if candidate is in dictionary
            if candidate in dictionary[current[0]]:
                a_lst.append(candidate)
                print('Found: ' + candidate)
                # tell user the program is searching for anagram
                print('Searching...')
            # check next word combination
            else:
                return
    else:
        for i in range(len(lst)):
            ele = lst[i]
            # choose
            if len(current) == 0:
                current.append(ele)
            else:
                word = word_processor(current)
                # if there's a word come with current initial, will continue explore
                if has_prefix(word):
                    current.append(ele)
                else:
                    return
            # Explore
            find_anagrams_helper(lst[:i]+lst[i+1:], target, current, a_lst)
            # un-choose
            current.pop()


def word_processor(current):
    """
    :param current: lst, store the new order of the characters provide by user
    :return string: str, string version of current
    """
    string = ''
    for i in range(len(current)):
        ch = current[i]
        string += ch
    return string


def has_prefix(test_word):
    """
    :param test_word: str, the possible anagram word
    :return: bool, whether any word in dictionary begin with test_word
    """
    initial = test_word[0]
    if initial in dictionary:
        if len(test_word) == 1:
            return True
        else:
            for word in dictionary[initial]:
                if word.startswith(test_word):
                    return True
    return False


if __name__ == '__main__':
    main()
