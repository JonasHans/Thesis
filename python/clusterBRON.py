# Sklearn modules
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import numpy as np

# Utils
from indexBRON import indexBRON, UNIQUE_IDENTIFIER
from utils.timeit import timeit

import matplotlib.pyplot as plt

# clustering based on: https://towardsdatascience.com/unsupervised-learning-with-python-173c51dc7f03
# TODO: https://machinelearningmastery.com/feature-selection-machine-learning-python/
@timeit
def cluster(dataset, algorithm):
	# Retrieve only the integer features
	intSet = dataset.loc[:,['MND_NUMMER','ANTL_PTJ', 'MAXSNELHD', 'HECTOMETER']]

	if algorithm == 'TSNE':
		# Defining Model
		model = TSNE(learning_rate=100)

		# Fitting Model
		transformed = model.fit_transform(intSet)

		# Plotting 2d t-Sne
		x_axis = transformed[:, 0]
		y_axis = transformed[:, 1]

		plt.scatter(x_axis, y_axis, c='g')
		plt.savefig('../results/cluster-TSNE-'+UNIQUE_IDENTIFIER+'.png')
	elif algorithm == 'KMEANS':
		# Defining Model
		model = KMeans(n_clusters=4).fit(intSet.head(40))
		print(model.labels_)

@timeit
def main():
	# Index BRON dataset
	[bron_ongevallen] = indexBRON()

	cluster(bron_ongevallen, 'KMEANS')

if __name__== "__main__":
	main()
