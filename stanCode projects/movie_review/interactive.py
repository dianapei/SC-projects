"""
File: interactive.py
Name: Pei-Rung Yu
------------------------
This file uses the function interactivePrompt
from util.py to predict the reviews input by 
users through Console. Remember to read the weights
and build a Dict[str: float]
"""

import util
import submission


def main():
	weights = {}
	# get weight from file weights.py
	with open('weights', 'r', encoding='utf-8') as w:
		for line in w:
			line = line.split()
			weights[line[0]] = float(line[1])
	util.interactivePrompt(featureExtractor=submission.extractWordFeatures, weights=weights)


if __name__ == '__main__':
	main()