# %% [markdown]
# # Adaboosting in Python.

# %%
# Import necessary datasets:

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# %%


# %%
# Create a synthetic dataset for binary classification using the make_classification function from sklearn.datasets:

# %%
X, y = make_classification(n_samples=1000, n_features=20, n_informative=10, n_redundant=0, random_state=42)


# %%


# %%
# Split the data into train and testing.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# %%
# create an AdaBoost classifier with decision tree as the base estimator:


# %%
base_estimator = DecisionTreeClassifier(max_depth=1)
n_estimators = 100
learning_rate = 1.0
ada_boost = AdaBoostClassifier(base_estimator=base_estimator, n_estimators=n_estimators, learning_rate=learning_rate, random_state=42)


# %%
# fit the AdaBoost classifier on the training data:

# %%
ada_boost.fit(X_train, y_train)


# %%
# make predictions on the testing data and calculate the accuracy


y_pred = ada_boost.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")


# %%


# %%


# %% [markdown]
# # Agglomerative Hierarchical Clustering.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.metrics import silhouette_score
import scipy.cluster.hierarchy as shc


# %%
# Loading and clearning data:

X = pd.read_csv('Credit_Card_Clustering_DataSet.csv')

# Dropping the CUST_ID column from the data
X = X.drop('CUST_ID', axis = 1)

# Handling the missing values
X.fillna(method ='ffill', inplace = True)


# %%
# Preprocessing the data.

# Scaling the data so that all the features become comparable
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Normalizing the data so that the data approximately
# follows a Gaussian distribution
X_normalized = normalize(X_scaled)

# Converting the numpy array into a pandas DataFrame
X_normalized = pd.DataFrame(X_normalized)


# %%
# Performing PCA for dimensionality reduction.

pca = PCA(n_components = 2)
X_principal = pca.fit_transform(X_normalized)
X_principal = pd.DataFrame(X_principal)
X_principal.columns = ['P1', 'P2']


# %%
# Visualize dendograms

plt.figure(figsize =(8, 8))
plt.title('Visualising the data')
Dendrogram = shc.dendrogram((shc.linkage(X_principal, method ='ward')))


# %%
# Visualize for different numbers of clusters:


# k = 2
ac2 = AgglomerativeClustering(n_clusters = 2)

# Visualizing the clustering
plt.figure(figsize =(6, 6))
plt.scatter(X_principal['P1'], X_principal['P2'],
		c = ac2.fit_predict(X_principal), cmap ='rainbow')
plt.show()


# %%
ac6 = AgglomerativeClustering(n_clusters = 4)

plt.figure(figsize =(6, 6))
plt.scatter(X_principal['P1'], X_principal['P2'],
			c = ac6.fit_predict(X_principal), cmap ='rainbow')
plt.show()



# %%
# For K = 6
ac6 = AgglomerativeClustering(n_clusters = 6)

plt.figure(figsize =(6, 6))
plt.scatter(X_principal['P1'], X_principal['P2'],
			c = ac6.fit_predict(X_principal), cmap ='rainbow')
plt.show()


# %%


# %%


# %%
# # Silhoutte's scores for dofferent numbers of clusters.
# 
# k = [2, 3, 4, 5, 6]
# 
# # Appending the silhouette scores of the different models to the list
# silhouette_scores = []
# silhouette_scores.append(
# 		silhouette_score(X_principal, ac2.fit_predict(X_principal)))
# silhouette_scores.append(
# 		silhouette_score(X_principal, ac3.fit_predict(X_principal)))
# silhouette_scores.append(
# 		silhouette_score(X_principal, ac4.fit_predict(X_principal)))
# silhouette_scores.append(
# 		silhouette_score(X_principal, ac6.fit_predict(X_principal)))
# 
# # Plotting a bar graph to compare the results
# plt.bar(k, silhouette_scores)
# plt.xlabel('Number of clusters', fontsize = 20)
# plt.ylabel('S(i)', fontsize = 20)
# plt.show()


# %%


# %% [markdown]
# # Divisive Clustering

# %%
import numpy as np
import matplotlib.pyplot as plt

# generate random dataset
np.random.seed(0)
X1 = np.random.randn(50, 2)
X2 = np.random.randn(50, 2) + np.array([5, 5])
X = np.vstack((X1, X2))



# %%

# implement divisive clustering
def divisive_clustering(X, k):
    clusters = [X] # start with all data points in one cluster
    while len(clusters) < k:
        max_index = 0
        max_cost = 0
        for i in range(len(clusters)):
            cluster = clusters[i]
            if len(cluster) == 1:
                continue
            # compute cost of dividing the cluster
            center = np.mean(cluster, axis=0)
            cost = np.sum((cluster - center) ** 2)
            # keep track of cluster with maximum cost
            if cost > max_cost:
                max_cost = cost
                max_index = i
        # split cluster with maximum cost
        cluster = clusters.pop(max_index)
        center = np.mean(cluster, axis=0)
        dists = np.sum((cluster - center) ** 2, axis=1)
        cluster1 = cluster[dists <= max_cost/2]
        cluster2 = cluster[dists > max_cost/2]
        clusters.append(cluster1)
        clusters.append(cluster2)
    return clusters


# %%

# perform divisive clustering on dataset
k = 2
clusters = divisive_clustering(X, k)


# %%
import matplotlib.pyplot as plt
# plot clusters
colors = ['b', 'r']
for i in range(k):
    cluster = clusters[i]
    plt.scatter(cluster[:,0], cluster[:,1], c=colors[i])
plt.show()

# %%


# %%



