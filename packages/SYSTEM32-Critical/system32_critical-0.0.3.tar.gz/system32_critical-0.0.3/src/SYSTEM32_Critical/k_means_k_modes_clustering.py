# %% [markdown]
# # Clustering Algorithms (K Means and K modes)

# %% [markdown]
# ### DataSet Used: Mushroonm DataSet
# ### Aim: To Cluster the mushroom without any labels into two classes (poisonous and edible)
# 
# ##### And later, we can use the label to check how much accurate clustering has been done.

# %%
import pandas as pd
import numpy as np 


import matplotlib.pyplot as plt 
import seaborn as sns 


# %%
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics.cluster import rand_score, adjusted_rand_score, silhouette_score




# %%
# for K Means Clustering,
from sklearn.cluster import KMeans

# %%
# For k modes clustering, 
from kmodes.kmodes import KModes

# %%
mushroom_data = pd.read_csv('./mushroom_data.csv')

# %%
mushroom_data.head()

# %% [markdown]
# #### Drop the class attribute from the dataset

# %%
y = mushroom_data[['class']]
X = mushroom_data.drop(['class'], axis=1)
X.head()

# %%
X.info()

# %%
X.describe()[1:2]

# %% [markdown]
# #### Apply Label Encoding on the dataset.

# %%
label_encoder = preprocessing.LabelEncoder()
X_encoded = X.apply(label_encoder.fit_transform)
X_encoded.head()

# %% [markdown]
# ## K Modes Clustering

# %%
kmodes_model = KModes(n_clusters=2, init='Cao', verbose=1)

# %%
clusters = kmodes_model.fit_predict(X_encoded)

# %%
predictions = pd.DataFrame(clusters, columns=['predicted-label'])

# %%
predictions.value_counts().plot.bar()

# %%
predictions.value_counts().plot.pie(autopct='%1.0f%%')

# %%
X['Predictions'] = clusters

# %%
encoded_label = y.apply(label_encoder.fit_transform)
print(f'{y.iloc[0].values} is encoded as {encoded_label.iloc[0].values}')
print(f'{y.iloc[1].values} is encoded as {encoded_label.iloc[1].values}')


# %% [markdown]
# #### Calculating Evaluation Metrics

# %%
# Create  a new dataframe containing new predicted clusters and Actual clusters. 
Cluster = pd.DataFrame()
Cluster['Actual'] = encoded_label.values.reshape(1, -1).tolist()[0]
Cluster['Predictions'] = clusters

Cluster.value_counts(['Actual', 'Predictions'])

# %%
rand_index = rand_score(encoded_label.values.reshape(1, -1)[0], clusters)
print(f"The rand index is: {rand_index}")

# %%
adjusted_rand_index = adjusted_rand_score(encoded_label.values.reshape(1, -1)[0], clusters)
print(f'The adjusted rand score is: {adjusted_rand_index}')

# %%


# %% [markdown]
# ## K Means Clustering

# %%
kmeans_model = KMeans(init = "random", n_clusters=2)

# %%
kmeans_clusters = kmeans_model.fit_predict(X_encoded)

# %%
predictions_kmeans = pd.DataFrame(kmeans_clusters, columns=['predicted-label-Kmeans'])



# %%
predictions_kmeans.value_counts().plot.bar()

# %%
predictions_kmeans.value_counts().plot.pie(autopct='%1.0f%%')

# %%
X['Predictions_KMeans'] = kmeans_clusters

# %% [markdown]
# ##### Encoding is already done above during K Modes Clustering. So, no need to do again.

# %% [markdown]
# ### Calculating Evaluation Metrics

# %%
# Create  a new dataframe containing new predicted clusters and Actual clusters. 
Cluster_KMeans = pd.DataFrame()
Cluster_KMeans['Actual'] = encoded_label.values.reshape(1, -1).tolist()[0]
Cluster_KMeans['Predictions'] = kmeans_clusters

Cluster_KMeans.value_counts(['Actual', 'Predictions'])

# %%
rand_index_kmeans = rand_score(encoded_label.values.reshape(1, -1)[0], kmeans_clusters)
print(f"The rand index is: {rand_index_kmeans}")

# %%
adjusted_rand_index_kmeans = adjusted_rand_score(encoded_label.values.reshape(1, -1)[0], kmeans_clusters)
print(f'The adjusted rand score is: {adjusted_rand_index_kmeans}')


# %%


# %%



