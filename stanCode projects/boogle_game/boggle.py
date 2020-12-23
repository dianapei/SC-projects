"""
File: boggle.py
Name: Diana Pei Rung Yu
----------------------------------------
This program recursively finds all the word(s) within the 4 rows of letters provided by user.
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'


# global variable
dictionary = {}    # to save all the words in FILE


def main():
	"""
	This program will first get words in dictionary and then get 4 rows of letters from user.
	And use the location within rows to recursively find the possible word combination and look up in dictionary.
	will print letter combination that can be found in dictionary and in the end tell user how many it find.
	"""
	read_dictionary()
	# get the 4 rows of letter from user
	rows = get_row()
	word_lst = []
	# use (column number, row number) to represent the letters in rows
	rows_locate = get_location(rows)
	# use recursion to find word
	find_word(rows_locate, rows, [], word_lst)
	# print the total of valid words are found
	if len(word_lst) == 0:
		print(f'Cannot find any words :(')
	elif len(word_lst) == 1:
		print(f'There is 1 word in total!')
	else:
		print(f'There are {len(word_lst)} words in total!')


def get_location(rows):
	"""
	:param rows: lst, letter input from user
	:return locates: lst, tuples represent position of characters in rows
	"""
	locates = []
	for i in range(len(rows[0])):
		for j in range(len(rows)):
			locates.append((i, j))
	return locates


def find_word(rows_locate, rows, current, word_lst):
	"""
	:param rows_locate: lst, position of letters for combination try out
	:param rows: lst, letters got from user
	:param current: lst, to store the letter combination
	:param word_lst: lst, word that has been found
	:return: no return value
	"""
	# base case
	if len(current) >= 4:
		word = word_processor(current, rows)
		if word not in word_lst:
			# check if word in dictionary
			sub_dict = dictionary[word[0]]
			if word in sub_dict:
				print(f'Found: "{word}"')
				word_lst.append(word)
	# loop over rows_locate to find letter combination that in dictionary
	for ele in rows_locate:
		# avoid adding repeat location of word
		if ele not in current:
			# choose if there's nothing in current
			if len(current) == 0:
				current.append(ele)
			else:
				# turn current(lst of location tuples) into word
				word = word_processor(current, rows)
				# if there's a word come with current initial, will add new ele and go next round
				if has_prefix(word):
					current.append(ele)
				else:
					return
			# get neighbor and explore
			neighbor = get_neighbor(rows, ele)
			find_word(neighbor, rows, current, word_lst)
			# un choose
			current.pop()


def get_neighbor(rows, ele):
	"""
	:param rows: lst, letters get from user
	:param ele: lst, current letter position
	:return neighbor: lst, the location tuple next to ele
	"""
	neighbor = []
	# find valid location tuples that in 3x3 grid centered by ele
	for x in range(-1, 2):
		for y in range(-1, 2):
			test_x = ele[0] + x
			test_y = ele[1] + y
			# see if test_x and test_y within rows
			if 0 <= test_x < len(rows[0]) and 0 <= test_y < len(rows):
				if (test_x, test_y) != ele:
					neighbor.append((test_x, test_y))
	return neighbor


def word_processor(current, rows):
	"""
	:param current: lst, store the new order of the characters provide by user
	:param rows: lst, letters got from user
	:return: str, string/letter version of current
	"""
	string = ''
	for i in range(len(current)):
		ch = rows[current[i][0]][current[i][1]]
		string += ch
	return string


def get_row():
	"""
	this function will get valid row input from user
	:return lst_row: lst, characters in the order that provided by user to find words
	"""
	num_row = 0
	lst_row = []
	while True:
		# continue to ask user before we receive 4 rows of valid input
		if num_row < 4:
			row = input(f' {num_row+1} row of letters: ')
			# case insensitive
			row = row.lower()
			row_data_lst = []
			check = check_row(row, row_data_lst)
			# if the input from user is valid
			if check:
				# add characters to lst_row
				lst_row.append(row_data_lst)
				num_row += 1
			# stop the program if get invalid input from user
			else:
				break
		# get all 16 letters
		else:
			return lst_row


def check_row(row, row_data_lst):
	"""
	:param row: str, letters divided by blank space provided by user
	:param row_data_lst: lst, letters in row
	:return: bool, show whether the input from user follows our input standard
	"""
	if len(row) == 7:
		# check if the letters are separated by blank space orn ot
		if row[1] and row[3] and row[5] != " ":
			print('Illegal input')
			return False
		else:
			for i in range(len(row)):
				ch = row[i]
				is_alpha = ch.isalpha()
				if is_alpha:
					row_data_lst.append(ch)
			# see if number of letter we get is valid
			if len(row_data_lst) != 4:
				print('Illegal input')
				return False
			else:
				return True
	else:
		print('Illegal input')
		return False


def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
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


def has_prefix(test_word):
	"""
		:param test_word: str, the possible anagram word
		:return: bool, see if any word in dictionary come with word
	"""
	initial = test_word[0]
	if initial in dictionary:
		if len(test_word) == 1:
			return True
		else:
			# see if any word in dictionary come with word
			for word in dictionary[initial]:
				if word.startswith(test_word):
					return True
	return False


if __name__ == '__main__':
	main()