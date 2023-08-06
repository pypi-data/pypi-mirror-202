# %% [markdown]
# # Support Vector Machines

# %% [markdown]
# ### DataSet Used: Universal Bank DataSet
# ### Aim: To Apply SVM and classify whether a person will take personal Loan or not.
# 
# ##### Use various types of SVM Kernels and test the evaluation metrics of each.

# %%
import pandas as pd
import numpy as np 


import matplotlib.pyplot as plt 
import seaborn as sns 


# %%
from sklearn.svm import SVC, NuSVC
from sklearn.cluster import  kmeans_plusplus
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# %%
# Supress Warnings
import warnings
warnings.filterwarnings('always')

# %%
x = pd.read_csv("./Bank_Loan_Dataset.csv")

# %%
x.head()

# %%
x.columns.to_list()

# %%
x.info()

# %%
# X = x[['Age', 'Experience', 'Income', 'Family', 'CCAvg', 'Personal Loan', 'Education']]
X = x.loc[:, x.columns != 'Personal Loan']
y = x[['Personal Loan']]
X.describe()

# %%
# plt.figure()
# sns.pairplot(X.iloc[:500, :], hue="Education")
# plt.show()

# %%


# %%
# # X_reduced = x[["Annual Income (k$)", "Spending Score (1-100)"]]
# 
# X_reduced = x[["Annual Income (k$)", "Age"]]
# y = x["Gender"]

# %% [markdown]
# ## Target Attribute: Personal Loan

# %% [markdown]
# ##### Let's visualize how 'Personal Loan' Attribute varies with respect to other attributes. Since we are dealing with 2d scatterplots we can only view its relation with respect to 2 attributes at a time. 

# %% [markdown]
# #### Some sample plots are:

# %%

sns.scatterplot(x='Income', y='Age', hue='Personal Loan', data = x)

# %%

sns.scatterplot(x='Experience', y='Age', hue='Personal Loan', data = x)

# %%
# x.columns
sns.scatterplot(x='Income', y='Family', hue='Personal Loan', data = x)

# %% [markdown]
# ### Split the dataset into training and validation data.

# %% [markdown]
# ##### Here, I have choosen ratio 80:20

# %%
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# %%
print("Training set, dimensions of X: ", X_train.shape, " and y:", y_train.shape)
print("Testing Set, dimensions of X: ", X_test.shape, " and y:", y_test.shape)


# %% [markdown]
# # 1. Simple Linear SVM

# %%
svm_clf = SVC(kernel="linear")
svm_clf.fit(X_train, y_train)


# %%
predictions = svm_clf.predict(X_test)

predictions

# %%
print(classification_report(y_test, predictions))

# %% [markdown]
# ## 2. Non Linear and Kernel SVMs

# %% [markdown]
# ### Radial Basis Function (RBF) Kernel (Default)

# %%
svm_clf_rbf = SVC(kernel='rbf');
svm_clf_rbf.fit(X_train, y_train);


# %%
predictions_rbf = svm_clf_rbf.predict(X_test)
print(classification_report(y_train, svm_clf_rbf.predict(X_train)))

# %%


# %% [markdown]
# ### Sigmoid Kernel SVM

# %%
svm_clf_sigmoid = SVC(kernel="sigmoid")
svm_clf_sigmoid.fit(X_train, y_train)
predictions_svm_sigmoid = svm_clf_sigmoid.predict(X_test)
print(classification_report(predictions_svm_sigmoid, y_test))


# %%


# %% [markdown]
# ### Using Polynomial Kernel for SVM

# %%
svm_clf_non_linear_polynomial_kernel = SVC(kernel="poly")
svm_clf_non_linear_polynomial_kernel.fit(X_train, y_train.values.ravel())
predictions_polynomial_kernel = svm_clf_non_linear_polynomial_kernel.predict(X_test)
print(classification_report(predictions_polynomial_kernel, y_test))


# %%



