
import csv
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

from scipy.stats import boxcox

from scipy import stats



def plot_correlation():

	# train_list = []

	# with open('new_train.csv', encoding='utf-8') as csv_file:
	# 	csv_reader = csv.reader(csv_file, delimiter=',')

	# 	for row in csv_reader:
	# 		train_list.append(row)

	# train_numpy = np.array(train_list)[1:, :]

	# general_train_np = train_numpy[:, [6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 19]].astype(float)
	# y_np = train_numpy[:, -1].astype(int)

	data = pd.read_csv('new_train.csv', encoding='utf-8')

	df = data.iloc[:, [6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 19]]

	corr = df.corr()
	corr.style.background_gradient(cmap='coolwarm').set_precision(2)

	htmlCode = corr.to_html()

	file = open("df.html","w")
	file.write(htmlCode)
	file.close()


	#general_train_np[:, 7:10] = general_train_np[:, 7:10] / general_train_np[:, [6]]

	#general_train_np[:, 5], fitted_lambda1 = boxcox(general_train_np[:, 5], lmbda=None)
	#general_train_np[:, 6], fitted_lambda2 = boxcox(general_train_np[:, 6], lmbda=None)

	#general_train_np[:, 5:7] = (general_train_np[:, 5:7] - np.mean(general_train_np[:, 5:7], axis=0)) / np.std(general_train_np[:, 5:7], axis=0)
	#general_train_np[:, 5:7] = (general_train_np[:, 5:7] - np.amin(general_train_np[:, 5:7], axis=0)) / (np.amax(general_train_np[:, 5:7], axis=0) - np.amin(general_train_np[:, 5:7], axis=0))

	#general_train_np[:, 10] = general_train_np[:, 10] / 5
	#general_train_np = (general_train_np - np.mean(general_train_np, axis=0)) / np.std(general_train_np, axis=0)

	



if __name__ == "__main__":

	plot_correlation()

