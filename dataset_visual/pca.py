
import csv
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

from scipy.stats import boxcox

from scipy import stats



def plot_pca():

	train_list = []

	with open('new_val.csv', encoding='utf-8') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')

		for row in csv_reader:
			train_list.append(row)

	train_numpy = np.array(train_list)[1:, :]

	general_train_np = train_numpy[:, [6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 19]].astype(float)
	y_np = train_numpy[:, -1].astype(int)

	general_train_np[:, 7:10] = general_train_np[:, 7:10] / general_train_np[:, [6]]

	general_train_np[:, 5], fitted_lambda1 = boxcox(general_train_np[:, 5], lmbda=None)
	general_train_np[:, 6], fitted_lambda2 = boxcox(general_train_np[:, 6], lmbda=None)

	#general_train_np[:, 5:7] = (general_train_np[:, 5:7] - np.mean(general_train_np[:, 5:7], axis=0)) / np.std(general_train_np[:, 5:7], axis=0)
	#general_train_np[:, 5:7] = (general_train_np[:, 5:7] - np.amin(general_train_np[:, 5:7], axis=0)) / (np.amax(general_train_np[:, 5:7], axis=0) - np.amin(general_train_np[:, 5:7], axis=0))

	#general_train_np[:, 10] = general_train_np[:, 10] / 5
	#general_train_np = (general_train_np - np.mean(general_train_np, axis=0)) / np.std(general_train_np, axis=0)

	for i in range(11):
		print(min(general_train_np[:, i]), max(general_train_np[:, i]))
	
	pca_11 = PCA(n_components=11, random_state=100)
	pca_11.fit(general_train_np)
	train_pca_11 = pca_11.transform(general_train_np)

	print(train_pca_11.shape)
	print(sum(pca_11.explained_variance_ratio_))
	print(pca_11.explained_variance_ratio_)

	
	pca_2 = PCA(n_components=2, random_state=100)
	pca_2.fit(general_train_np)
	train_pca_2 = pca_2.transform(general_train_np)

	

	plt.scatter(train_pca_2[y_np==1, 0], train_pca_2[y_np==1, 1])
	plt.scatter(train_pca_2[y_np==0, 0], train_pca_2[y_np==0, 1])
	plt.legend(['trending video', 'non-trending video'])
	plt.xlabel('First principal component')
	plt.ylabel('Second principal component')

	plt.show()



if __name__ == "__main__":

	plot_pca()