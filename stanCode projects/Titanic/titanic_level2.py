"""
File: titanic_level2.py
Name: Pei-Rung Yu
----------------------------------
This file builds a machine learning algorithm by pandas and sklearn libraries.
We'll be using pandas to read in dataset, store data into a DataFrame,
standardize the data by sklearn, and finally train the model and
test it on kaggle. Hyperparameters are hidden by the library!
This abstraction makes it easy to use but less flexible.
You should find a good model that surpasses 77% test accuracy on kaggle.
"""

import math
import pandas as pd
from sklearn import preprocessing, linear_model
TRAIN_FILE = 'titanic_data/train.csv'
TEST_FILE = 'titanic_data/test.csv'


def data_preprocess(filename, mode='Train', training_data=None):
	"""
	:param filename: str, the filename to be read into pandas
	:param mode: str, indicating the mode we are using (either Train or Test)
	:param training_data: DataFrame, a 2D data structure that looks like an excel worksheet
						  (You will only use this when mode == 'Test')
	:return: Tuple(data, labels), if the mode is 'Train'
			 data, if the mode is 'Test'
	"""
	data = pd.read_csv(filename)
	labels = None
	if mode == 'Train':
		data = data[['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']].dropna()
		labels = data.Survived

	elif mode == 'Test':
		# Fill in the NaN cells by the values in nan_cache to make it consistent
		data['Fare'] = data['Fare'].fillna(round(training_data['Fare'].mean(), 3))
		data['Age'] = data['Age'].fillna(round(training_data['Age'].mean(), 3))

	# Changing 'male' to 1, 'female' to 0
	data.loc[data.Sex == 'male', 'Sex'] = 1
	data.loc[data.Sex == 'female', 'Sex'] = 0

	# Changing 'S' to 0, 'C' to 1, 'Q' to 2
	data.loc[data.Embarked == 'S', 'Embarked'] = 0
	data.loc[data.Embarked == 'C', 'Embarked'] = 1
	data.loc[data.Embarked == 'Q', 'Embarked'] = 2

	data = data[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]

	if mode == 'Train':
		return data, labels
	elif mode == 'Test':
		return data


def one_hot_encoding(data, feature):
	"""
	:param data: DataFrame, key is the column name, value is its data
	:param feature: str, the column name of interest
	:return data: DataFrame, remove the feature column and add its one-hot encoding features
	"""
	if feature == 'Sex':
		# one hot encoding for new categories Sex_0 & Sex_1 and delete Sex Column
		data['Sex_0'] = 0
		data.loc[data.Sex == 0, 'Sex_0'] = 1
		data['Sex_1'] = 0
		data.loc[data.Sex == 1, 'Sex_1'] = 1
		data.pop('Sex')

	elif feature == 'Pclass':
		# one hot encoding for new categories Pclass_0, Pclass_1 & Pclass_2 and delete Pclass Column
		data['Pclass_0'] = 0
		data.loc[data.Pclass == 1, 'Pclass_0'] = 1
		data['Pclass_1'] = 0
		data.loc[data.Pclass == 2, 'Pclass_1'] = 1
		data['Pclass_2'] = 0
		data.loc[data.Pclass == 3, 'Pclass_2'] = 1
		data.pop('Pclass')

	elif feature == 'Embarked':
		# one hot encoding for new categories Embarked_0, Embarked_1 & Embarked_2 and delete Embarked Column
		data['Embarked_0'] = 0
		data.loc[data.Embarked == 0, 'Embarked_0'] = 1
		data['Embarked_1'] = 0
		data.loc[data.Embarked == 1, 'Embarked_1'] = 1
		data['Embarked_2'] = 0
		data.loc[data.Embarked == 2, 'Embarked_1'] = 1
		data.pop('Embarked')

	return data


def standardization(data, mode='Train'):
	"""
	:param data: DataFrame, key is the column name, value is its data
	:param mode: str, indicating the mode we are using (either Train or Test)
	:return data: DataFrame, standardized features
	"""
	standarizer = preprocessing.StandardScaler()
	if mode == 'Train':
		data = standarizer.fit_transform(data)
	else:
		data = standarizer.transform(data)

	return data


def main():
	"""
	You should call data_preprocess(), one_hot_encoding(), and
	standardization() on your training data. You should see ~80% accuracy
	on degree1; 83% on degree2; ~85% on degree3
	TODO: real accuracy on degree1 -> 0.80196629
	TODO: real accuracy on degree2 -> 0.83426966
	TODO: real accuracy on degree3 -> 0.85393258
	"""

	for i in range(3):
		# Train & Test data preprocess
		train_data, label = data_preprocess(TRAIN_FILE)
		test_data = data_preprocess(TEST_FILE, mode='Test', training_data=train_data)

		train_data = one_hot_encoding(train_data, 'Sex')
		train_data = one_hot_encoding(train_data, 'Pclass')
		train_data = one_hot_encoding(train_data, 'Embarked')

		test_data = one_hot_encoding(test_data, 'Sex')
		test_data = one_hot_encoding(test_data, 'Pclass')
		test_data = one_hot_encoding(test_data, 'Embarked')

		# Degree 2 & 3 Polynomial
		if i > 0:
			poly_feature_extractor = preprocessing.PolynomialFeatures(degree=i+1)
			train_data = poly_feature_extractor.fit_transform(train_data)
			test_data = poly_feature_extractor.transform(test_data)

		# Standardization
		standardizer = preprocessing.StandardScaler()
		train_data = standardizer.fit_transform(train_data)
		test_data = standardizer.transform(test_data)

		# Training
		h = linear_model.LogisticRegression(max_iter=10000)
		classifier = h.fit(train_data, label)
		acc = classifier.score(train_data, label)
		print(f'Degree {i+1} Training Acc: {acc}')

		# Testing
		predictions = classifier.predict(test_data)
		test(predictions, f'Pei_asgmt3_level2_degree{i+1}.csv')


def test(predictions, filename):
	with open(filename, 'w') as out:
		out.write('PassengerId,Survived\n')
		start_id = 892
		for ans in predictions:
			out.write(str(start_id)+','+str(ans)+'\n')
			start_id += 1



if __name__ == '__main__':
	main()
