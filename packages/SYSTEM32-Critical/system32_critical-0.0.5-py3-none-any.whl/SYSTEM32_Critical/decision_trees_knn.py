# %% [markdown]
# ### 2
# 
# 
# - Decision Trees (ID3) based on Entropy
# - Decision Trees (CART) based on Gini Index
# - K Nearest Neighbour (KNN) Classification
# 
# 

# %% [markdown]
# ### Import all necessary Libraries

# %%
# Libraries to load / import data & perform basic explorations.

from sklearn import datasets as ds

import pandas as pd
import numpy as np

# %%
# Libraries to perform Data Split, Training, and Evaluation
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn import metrics

# Library for Cross validation in KNN Classification
from sklearn.model_selection import cross_val_score


# %%
# Libraries to enable Tree Visualization

from sklearn.tree import export_graphviz
from six import StringIO

from IPython.display import Image
import pydotplus

# %%
# Libaries for KNN Classification

from sklearn.neighbors import KNeighborsClassifier

# Libary for KNN Parameter Tuning visualization

import matplotlib.pyplot as plt
import seaborn as sns

# %%


# %% [markdown]
# ### Load the Internally available iris dataset from sklearn datasets

# %%
x = ds.load_iris()

# %%
x

# %%


# %%
x['feature_names'] + ['target']

# %%
type(x)

# %%
x.keys()

# %%
dataset = pd.DataFrame(
    data = np.c_[x['data'], x['target']],
    columns = x['feature_names'] + ['target']
)

# %%
dataset.head()

# %%
dataset.info()

# %%
dataset.describe()

# %%
dataset.columns

# %%
plt.figure()
sns.pairplot(dataset, hue = "target", size=3, markers=["o", "s", "D"])
plt.show()

# %% [markdown]
# # Decision Trees

# %% [markdown]
# ### ID3 Tree

# %%
# Separate the other training attributes and target class attributes

X_id3 = dataset.iloc[:,0:4 ]
y_id3 = dataset.iloc[:, 4:5]

# %%
X_id3.head()

# %%
y_id3.head()

# %%
# split the data into train and test in the ratio 80% : 20%
X_id3_train, X_id3_test, y_id3_train, y_id3_test = train_test_split(X_id3, y_id3, train_size=0.8, random_state=7)

# %%
# Create a decision tree object based on "Entropy" for ID3 algorithm
clf_id3 = DecisionTreeClassifier(criterion="entropy")


# %%
# Fit the training data on the ML model object
clf_id3.fit(X_id3_train, y_id3_train)

# %%
# Perform prediction using the testing data.

y_id3_pred = clf_id3.predict(X_id3_test)

# %%
# Compute accuracy score from the predictions and actual classes
acc = metrics.accuracy_score(y_id3_test, y_id3_pred)

print("The acccuracy score is: ", acc)

# %%
# More detailed validation results
print(metrics.classification_report(y_true = y_id3_test, y_pred = y_id3_pred))

# %%


# %%
# Function to construct a figure of the decision tree model and save it locally as given filename.
def view_tree(model, features, target_classes, tree_name = 'file.png'):

    dot_data = StringIO()

    export_graphviz(model, out_file=dot_data, filled=True, rounded=True, special_characters=True, feature_names=features, class_names=class_labels)

    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

    graph.write_png(tree_name)

    return graph


# %%
features = dataset.columns.tolist()[:-1]
class_labels = ['0.0', '1.0', '2.0']

# %%
# Construct a tree by calling the earlier function, save the tree as a png file and display it inline.

id3_tree = view_tree(clf_id3, features=features, target_classes=class_labels, tree_name='id3_tree.png')
Image(id3_tree.create_png())

# %%
# Alternative plotting technique.

plt.figure(figsize=(10,15))
tree.plot_tree(clf_id3)


# %%


# %% [markdown]
# # Decision Trees (CART)

# %%


# %%
# Separate the other training attributes and target class attributes for training ML model using CART algorithm

X_cart = dataset.iloc[:,0:4 ]
y_cart = dataset.iloc[:, 4:5]

# %%
X_cart.head()

# %%
y_cart.head()

# %%
# split the data into train and test in the ratio 80% : 20%

X_cart_train, X_cart_test, y_cart_train, y_cart_test = train_test_split(X_cart, y_cart, train_size=0.8, random_state=42)

# %%
# Create a decision tree object based on "Gini Index" for CART algorithm

clf_cart = DecisionTreeClassifier(criterion="gini")


# %%
# Fit the training data on the CART ML model object

clf_cart.fit(X_cart_train, y_cart_train)

# %%
# Perform prediction using the testing data.

y_cart_pred = clf_cart.predict(X_cart_test)

# %%
# Compute accuracy score from the predictions and actual classes

acc = metrics.accuracy_score(y_cart_test, y_cart_pred)

print("The acccuracy score is: ", acc)

# %%
# More detailed validation results

print(metrics.classification_report(y_true = y_cart_test, y_pred = y_cart_pred))

# %%


# %%
# Function to construct a figure of the decision tree model and save it locally as given filename.
def view_tree(model, features, target_classes, tree_name = 'file.png'):

    dot_data = StringIO()

    export_graphviz(model, out_file=dot_data, filled=True, rounded=True, special_characters=True, feature_names=features, class_names=class_labels)

    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

    graph.write_png(tree_name)

    return graph


# %%
features = dataset.columns.tolist()[:-1]
class_labels = ['0.0', '1.0', '2.0']

# %%
# Construct a tree by calling the earlier function, save the tree as a png file and display it inline.

id3_tree = view_tree(clf_cart, features=features, target_classes=class_labels, tree_name='cart_tree.png')
Image(id3_tree.create_png())

# %%


# %% [markdown]
# ### KNN Clustering

# %%


# %%
# Separate the other training attributes and target class attributes for training a classification model using KNN 

X_knn = dataset.iloc[:,0:4 ]
y_knn = dataset.iloc[:, 4:5]

# %%
X_knn.head()

# %%
y_knn.head()

# %%
# Split the data into train and test in the ratio 80% : 20%

X_knn_train, X_knn_test, y_knn_train, y_knn_test = train_test_split(X_knn, y_knn, train_size=0.8)

# %%

# Create an object of KNN Model
knn = KNeighborsClassifier(n_neighbors=2)

# With my initial knowledge about the data, I have taken initial approximation of the number of neighbours as 3

# %%
# Fit the training data on the KNN classification model
classifier = knn.fit(X_knn_train, y_knn_train)



# %%
# Predicting the Test set results
y_knn_pred = classifier.predict(X_knn_test)

# %%


# %%
# Display the detailed model evaluation results
cm = metrics.classification_report(y_knn_test, y_knn_pred)
print(cm)

# %% [markdown]
# #### Find optimal number of classes by tuning parameters (using cross validation)

# %%
# creating list of K (number of classes) for KNN
k_list = list(range(3,20,1))


# %%
# creating list of cross validation scores
cross_val_scores = []


# %%
# perform 10-fold cross validation
for k in k_list:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_knn_train, y_knn_train.values.ravel(), cv=10, scoring='accuracy')
    cross_val_scores.append(scores.mean())

# %%
cross_val_scores

# %%
# changing to misclassification error

# display Mis classification Errors for each number of classes

MSE = [x for x in cross_val_scores]

plt.figure()
plt.figure(figsize=(15,10))
plt.title('The optimal number of neighbors', fontsize=20, fontweight='bold')
plt.xlabel('Number of Neighbors K', fontsize=15)
plt.ylabel('Misclassification Error', fontsize=15)
sns.set_style("whitegrid")
plt.plot(k_list, MSE)

plt.show()

# %%
# here, the optimal number of classes is found as 6 due to the lowest missclassification rate.

# %%


# %%


# %%


# %%



