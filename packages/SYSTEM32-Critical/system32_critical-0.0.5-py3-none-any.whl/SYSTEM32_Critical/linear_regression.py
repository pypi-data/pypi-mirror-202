# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
# Simple Linear Regression Code.
dataset = pd.read_csv('salary_data.csv')

x = dataset.iloc[:, 0: -1].values
y = dataset.iloc[:,-1].values


# %%
dataset.info()

# %%
dataset.plot(x='YearsOfExperience', y='Salary', style='o')


# %%
from sklearn.model_selection import train_test_split

# %%
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=7)

# %%
Train_Set, Test_Set = train_test_split(x, test_size=0.2)

# %%
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(x_train, y_train)


# %%
print("The intercept of straight line is: ", model.intercept_)

# %%
print("The slope of line is: ", model.coef_)

# %%
x = float(input("Entee the Years of Experience: "))

# %%
print("The predicted salary after %.0f years of Experience is: " %x, end="")
print(" %.2f" %model.predict(X=np.array([x]).reshape(-1,1)))

# %%
# Perform prediction on the test data.

y_pred = model.predict(x_test)
y_pred

# %%


# %%
# Display scatter plot of expected values with predicted values.

plt.title("Prediction Instances in simple Linear regression")
plt.xlabel("Experience")
plt.ylabel("Salary")

plt.scatter(x_test, y_test, color = 'blue')

plt.plot(x_test, model.predict(x_test), color = "red")
plt.show()



# %%

# Display scatter plot of test data with prediction on train data.

plt.title("Training instances in simple Linear regression")
plt.xlabel("Experience")
plt.ylabel("Salary")

plt.scatter(x_test, y_test, color = 'blue')

plt.plot(x_train, model.predict(x_train), color = "red")
plt.show()

# %%
# Performance Evaluation using RMSE

from sklearn.metrics import mean_squared_error
print("Mean squared error of the Simple Linear Regression model is: %.2f" %mean_squared_error(y_test, y_pred))


# %%



