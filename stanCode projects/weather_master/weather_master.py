"""
File: weather_master.py
-----------------------
This program should implement a console program
that asks weather data from user to compute the
average, highest, lowest, cold days among the inputs.
Output format should match what is shown in the sample
run in the Assignment 2 Handout.
"""

EXIT = -1


def main():
	"""
	This program will tell the highest, lowest, average and how many cold days (temperature below 16)
	of the inputs provided by the user.
	"""
	print("StanCode \"Weather Master 4.0\"!")
	count = 0
	total = 0
	highest = 0
	lowest = 0
	low_alert = 0
	# continue to ask for input until the program gets the exit value
	while True:
		temperature = int(input("Next Temperature: (or "+str(EXIT)+" to quit)? "))
		# assign first input to be "highest temperature" and "lowest temperature" to make comparison afterwards
		if count == 0:
			highest = temperature
			lowest = temperature
		# this program will stop if the input equals to the exit value
		if temperature == EXIT:
			# this program will provide different info based on it gets exit value only or not
			if count == 0:
				print("No temperature were entered.")
				break
			# will tell the average, highest, lowest and cold days among the input
			else:
				print("Highest temperature = " + str(highest))
				print("Lowest temperature = " + str(lowest))
				print("Average = "+str(average))
				print(str(low_alert) + " cold day(s)")
				break
		else:
			# count how many times it receives input
			count += 1
			# calculate the sum of the input(s)
			total = total + temperature
			# calculate the average of the input(s)
			average = total / count
			# cold day number will increase 1 if the input is below 16
			if temperature < 16:
				low_alert += 1
			# compare input with the lowest temperature among past input(s)
			if temperature < lowest:
				lowest = temperature
			# compare input with the highest temperature among past input(s)
			elif temperature > highest:
				highest = temperature


###### DO NOT EDIT CODE BELOW THIS LINE ######

if __name__ == "__main__":
	main()
