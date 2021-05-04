"""
File: titanic.py
Name: Pei-Rung Yu
----------------------------------
This file builds a machine learning algorithm from scratch 
by Python codes. We'll be using 'with open' to read in dataset,
store data into a Python dict, and finally train the model and 
test it on kaggle. This model is the most flexible one among all
levels. You should do hyperparameter tuning and find the best model.
"""

import math
TRAIN_FILE = 'titanic_data/train.csv'
TEST_FILE = 'titanic_data/test.csv'
from collections import defaultdict


def data_preprocess(filename: str, data: dict, mode='Train', training_data=None):
	"""
	:param filename: str, the filename to be processed
	:param data: dict[str: list], key is the column name, value is its data
	:param mode: str, indicating the mode we are using
	:param training_data: dict[str: list], key is the column name, value is its data
						  (You will only use this when mode == 'Test')
	"""
	data = defaultdict(list)
	with open(filename, 'r') as f:
		first = True
		for line in f:
			if first:
				first = False
			else:
				line = line.split(',')
				if mode == 'Train':
					# while training, only take data without missing
					if line[6].find('.') != -1 or line[6].isdigit() and line[12].strip().isalpha():
						feature_vector, y = feature_extractor(line, mode, training_data)
						data['Survived'].append(y)
						data['Pclass'].append(feature_vector[0])
						data['Sex'].append(feature_vector[1])
						data['Age'].append(feature_vector[2])
						data['SibSp'].append(feature_vector[3])
						data['Parch'].append(feature_vector[4])
						data['Fare'].append(feature_vector[5])
						data['Embarked'].append(feature_vector[6])
				else:
					feature_vector = feature_extractor(line, mode, training_data)
					data['Pclass'].append(feature_vector[0])
					data['Sex'].append(feature_vector[1])
					data['Age'].append(feature_vector[2])
					data['SibSp'].append(feature_vector[3])
					data['Parch'].append(feature_vector[4])
					data['Fare'].append(feature_vector[5])
					data['Embarked'].append(feature_vector[6])
	return data


def feature_extractor(line, mode, training_data):
	"""
	: param line: str, the line of data extracted from the training set
	: param training_data: dict[str: list], key is the column name, value is its data (use this when mode == 'Test')
	: return: Tuple(list, label), the feature vector and the true label
	"""
	# [Id, Surv, Pclass, F_Name, L_Name, Sex5, Age, SibSp, ParCh, Ticket, Fare10, Cabin, Embarked]
	ans = []
	if mode == 'Train':
		y = int(line[1])
		start = 2
	else:
		y = -1
		start = 1
	for i in range(len(line)):
		if i == start:
			# Pclass
			ans.append(int(line[i]))
		elif i == start + 3:
			# Gender
			if line[i] == 'male':
				ans.append(1)
			else:
				ans.append(0)
		elif i == start + 4:
			# Age
			if line[i].find('.') != -1 or line[i].isdigit():
				ans.append(float(line[i]))
			else:
				ans.append(math.fsum(training_data['Age'])/len(training_data['Age']))
		elif i == start + 5:
			# SibSp
			ans.append(int(line[i]))
		elif i == start + 6:
			# Parch
			ans.append(int(line[i]))
		elif i == start + 8:
			# Fare
			if line[i].find('.') != -1 or line[i].isdigit():
				ans.append(float(line[i]))
			else:
				ans.append(round(math.fsum(training_data['Fare'])/len(training_data['Fare']), 3))
		elif i == start + 10:
			# Embarked
			if line[i].strip() == 'S':
				ans.append(0)
			elif line[i].strip() == 'C':
				ans.append(1)
			elif line[i].strip() == 'Q':
				ans.append(2)
	if mode == 'Train':
		return ans, y
	return ans


def one_hot_encoding(data: dict, feature: str):
	"""
	:param data: dict[str, list], key is the column name, value is its data
	:param feature: str, the column name of interest
	:return data: dict[str, list], remove the feature column and add its one-hot encoding features
	"""
	if feature == 'Sex':
		for i in range(len(data[feature])):
			if data[feature][i] == 1:
				data['Sex_1'].append(1)
				data['Sex_0'].append(0)
			else:
				data['Sex_1'].append(0)
				data['Sex_0'].append(1)

	elif feature == 'Pclass':
		for j in range(len(data[feature])):
			if data[feature][j] == 1:
				data['Pclass_0'].append(1)
				data['Pclass_1'].append(0)
				data['Pclass_2'].append(0)
			elif data[feature][j] == 2:
				data['Pclass_0'].append(0)
				data['Pclass_1'].append(1)
				data['Pclass_2'].append(0)
			elif data[feature][j] == 3:
				data['Pclass_0'].append(0)
				data['Pclass_1'].append(0)
				data['Pclass_2'].append(1)

	elif feature == 'Embarked':
		for k in range(len(data[feature])):
			if data[feature][k] == 0:
				data['Embarked_0'].append(1)
				data['Embarked_1'].append(0)
				data['Embarked_2'].append(0)
			elif data[feature][k] == 1:
				data['Embarked_0'].append(0)
				data['Embarked_1'].append(1)
				data['Embarked_2'].append(0)
			elif data[feature][k] == 2:
				data['Embarked_0'].append(0)
				data['Embarked_1'].append(0)
				data['Embarked_2'].append(1)

	data.pop(feature)
	return data


def normalize(data: dict):
	"""
	:param data: dict[str, list], key is the column name, value is its data
	:return data: dict[str, list], key is the column name, value is its normalized data
	"""
	for name in data:
		nor_value = []
		for value in data[name]:
			if value-min(data[name]) == 0 or max(data[name])-min(data[name]) == 0:
				nor_value.append(0)
			else:
				nor_value.append((value-min(data[name]))/(max(data[name])-min(data[name])))
		data[name] = nor_value
	return data


def learnPredictor(inputs: dict, labels: list, degree: int, num_epochs: int, alpha: float):
	"""
	:param inputs: dict[str, list], key is the column name, value is its data
	:param labels: list[int], indicating the true label for each data
	:param degree: int, degree of polynomial features
	:param num_epochs: int, the number of epochs for training
	:param alpha: float, known as step size or learning rate
	:return weights: dict[str, float], feature name and its weight
	"""
	# Step 1 : Initialize weights
	weights = {}  # feature => weight
	keys = list(inputs.keys())
	if degree == 1:
		for i in range(len(keys)):
			weights[keys[i]] = 0
	elif degree == 2:
		for i in range(len(keys)):
			weights[keys[i]] = 0
		for i in range(len(keys)):
			for j in range(i, len(keys)):
				weights[keys[i] + keys[j]] = 0

	# Step 2 : Start training
	for epoch in range(num_epochs):
		for i in range(len(labels)):
			# Step 3 : Feature Extract
			feature = defaultdict(list)
			if degree == 1:
				for j in range(len(keys)):
					feature[keys[j]] = inputs[keys[j]][i]
			else:
				for j in range(len(keys)):
					feature[keys[j]] = inputs[keys[j]][i]
					for k in range(j, len(keys)):
						feature[keys[j] + keys[k]] = inputs[keys[j]][i]*inputs[keys[k]][i]
			# Step 4 : Update weights
			y = labels[i]
			h = 1 / (1 + math.exp(-sum(feature[name]*weights[name] for name in feature)))
			for name in weights:
				weights[name] -= (alpha*(h-y)) * feature[name]
	return weights


def main():

	# Degree1 train & test data preprocess
	train_data = data_preprocess(TRAIN_FILE, {})
	test_data1 = data_preprocess(TEST_FILE, {}, mode='Test', training_data=train_data)

	train_data = one_hot_encoding(train_data, 'Sex')
	train_data = one_hot_encoding(train_data, 'Pclass')
	train_data = one_hot_encoding(train_data, 'Embarked')
	test_data1 = one_hot_encoding(test_data1, 'Sex')
	test_data1 = one_hot_encoding(test_data1, 'Pclass')
	test_data1 = one_hot_encoding(test_data1, 'Embarked')

	train_data = normalize(train_data)
	test_data1 = normalize(test_data1)
	labels = train_data.pop('Survived')
	labels = list(int(labels[i]) for i in range(len(labels)))

	# Degree1 Training
	weights1 = learnPredictor(train_data, labels, 1, 100, 0.1)

	# Degree1 Prediction
	predict(weights1, test_data1, 'titanic_degree1.csv')

	# Degree2 Training
	weights2 = learnPredictor(train_data, labels, 2, 100, 0.1)

	# Degree2 Testing
	test_data2 = make_degree2(test_data1)
	predict(weights2, test_data2, 'titanic_degree2.csv')


def make_degree2(test_data):
	"""
	:param test_data: dict[str:lst] key is the column name, value is its data
	:return: dict[str: lst] add degree 2 features of test_data
	"""
	keys = list(test_data.keys())
	for i in range(len(test_data['Age'])):
		for j in range(len(keys)):
			for k in range(j, len(keys)):
				test_data[keys[j] + keys[k]].append(test_data[keys[j]][i] * test_data[keys[k]][i])
	return test_data


def predict(weights, test_data, filename):
	"""
	:param weights: dict[str, float], feature name and its weight
	:param test_data: dict[str, lst], key is the column name, value is its data
	:param filename: str, name of the file to be created
	Predict result by extracting the features and getting the score of weight and test_data
	"""

	ans = []
	for i in range(len(test_data['Age'])):
		score = 0
		for feature in weights:
			score += weights[feature]*test_data[feature][i]
		ans.append(1) if score > 0 else ans.append(0)
	# Create file
	initial = 892
	with open(filename, 'w') as out:
		out.write('PassengerId' + ',' + 'Survived\n')
		for i in range(len(ans)):
			out.write(str(initial + i) + ',' + str(ans[i]) + '\n')

if __name__ == '__main__':
	main()
