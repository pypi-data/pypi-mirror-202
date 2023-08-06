# %% [markdown]
# # Find-S algorithm:
# 

# %%
# Import required Libraries 
# for numeric computation and array manipulations.

import pandas as pd
import numpy as np


# %%
# %%bash
# Creating the dataset to train Find s Algorithm

# Create a csv file of dataset called 'data.csv' 
# [ -e data.csv ] && rm data.csv

# touch data.csv


# Add the records into the csv file.
# echo 'citations,size,inlibrary,price,editions,buy' >> data.csv
# echo 'some,small,no,affordable,many,no' >> data.csv
# echo 'many,big,no,expensive,one,yes' >> data.csv
# echo 'some,big,always,expensive,few,no' >> data.csv
# echo 'many,medium,no,expensive,many,yes' >> data.csv
# echo 'many,small,no,affordable,many,yes' >> data.csv



# %%
# %%bash
# cat data.csv

# %%

#View  read the data in the csv file
data = pd.read_csv("data.csv")
print(data)


# %%
#making an numpy array of all the attributes
d = np.array(data)[:,:-1]
print("\n The attributes are: \n",d)

#segragating the target that has positive and negative examples
target = np.array(data)[:,-1]
print("\n The target is: ",target)


# %%

#training function to implement find-s algorithm

def train(c,t):
    for i, val in enumerate(t):
        if val == "yes":
            specific_hypothesis = c[i].copy()
            break
            
    for i, val in enumerate(c):
        if t[i] == "yes":
            for x in range(len(specific_hypothesis)):
                if val[x] != specific_hypothesis[x]:
                    specific_hypothesis[x] = '?'
                else:
                    pass
                
    return specific_hypothesis


# %%
#obtaining the final hypothesis
print("\n The final hypothesis is:",train(d,target))


# %% [markdown]
# ## Add a negative instance of data and train again.

# %%
# %%bash
# remove the data.csv file if already present.
# [ -e newdata.csv ] && rm newdata.csv

# Create new file add another instance of negative training data.
# cat data.csv >> newdata.csv
# echo 'many,small,always,expensive,many,no' >> newdata.csv

# %%
print("The data after adding a new instance is: \n", pd.read_csv('newdata.csv'))

new_train = np.array(pd.read_csv('newdata.csv'))[:, :-1]
labels = np.array(pd.read_csv('newdata.csv'))[:,-1]

print("\n Upon training on modified data, the new final hypothesis is:", train(new_train, labels))

# %% [markdown]
# Find S algorithm simply discards any negative instance.  
# 
# Hence, no effect of a negative training data is reflected on the final hypothesis.

# %% [markdown]
# ## Add a positive instance of data and train again.

# %%
# %%bash
# Add one more positive training data and train it.
# echo 'many,small,always,expensive,many,yes' >> newdata.csv

# %%
print("The data after adding a new instance is: \n", pd.read_csv('newdata.csv'))
new_train = np.array(pd.read_csv('newdata.csv'))[:, :-1]
labels = np.array(pd.read_csv('newdata.csv'))[:,-1]

print("\n Upon training on modified data, the new final hypothesis is:", train(new_train, labels))

# %% [markdown]
# Find S takes a positive instance into consideration for training. It matches all the attributes of the current instance with the hypothesis that has been obtained so far and forms a new hypothesis as a result. 
# 
# 
# Hence, change in final hypothesis is reflected after training on a new and different positive instance.

# %%


# %%


# %%


# %% [markdown]
# # Candidate Elimination Algorithm

# %%
# Read the training instances from the file: newdata.csv

candidate_elim_file = 'candidate_elim.csv'
concepts = np.array(pd.read_csv(candidate_elim_file))[:, :-1]
target = np.array(pd.read_csv(candidate_elim_file))[:, -1]

# %%
def candidate_elim_learn(concepts, target):

    print("Initialization of Specific and General Hypothesis")

    specific_h = concepts[0].copy()
    print("First Specific Hypothesis (S1): ",specific_h)

    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    print("General Hypothesis are (G0): ",general_h)
    
    print("\n\nConcepts are: ",concepts)

    for i, h in enumerate(concepts):

        if target[i] == "yes":
            for x in range(len(specific_h)):

                if h[x] != specific_h[x]:
                    specific_h[x] = '?'
                    general_h[x][x] = '?'

        if target[i] == "no":
            for x in range(len(specific_h)):

                if h[x] != specific_h[x]:
                    general_h[x][x] = specific_h[x]
                else:
                    general_h[x][x] = '?'

    print("\nSteps of Candidate Elimination Algorithm: ",i+1)

    print("Specific_h: ",i+1)
    print(specific_h,"\n")

    print("general_h :", i+1)
    print(general_h)

    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?']]

    print("\nIndices",indices)

    for i in indices:
        general_h.remove(['?', '?', '?', '?', '?'])

    return specific_h, general_h


# %%
s_final,g_final = candidate_elim_learn(concepts, target)

print("\nFinal Specific_h:", s_final, sep="\n")

print("Final General_h:", g_final, sep="\n")

# %%


# %%



