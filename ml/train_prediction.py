# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# # Importing DataSet
# * The Data Set is in excel file format so we use pandas read_excel to load the data.
# * After loading the data we check the data to see if any data is missing or contains null values in any rows or coloumns.
# * If any null values are observed than:
# 1. Imputing data using Imputataion in sklearn
# 2. Filling NaN values with either of mean , median or mode using fillna() method
# * Describe and plot data for proper understanding of data.

# %%
train_data = pd.read_excel(r"ml/Flight_data.xlsx")

# %%
pd.set_option("display.max_columns", None)

# %%
train_data.head()

# %%
train_data.shape

# %%
train_data.info()

# %%
train_data.dropna(inplace=True)

# %% [markdown]
# As we can see from above the Date and Time Feild has object data type. Hence it needs to be converted into time stamp for correctly using this data for prediction.
#
# We have <b>to_datetime</b> in pandas to convert object daattype to timestamp

# %% [markdown]
# <font color='cyan'>.dt.day method will extract only day of that date.<br>
# .dt.month method will extract only month of that date.</font>

# %%
train_data["Journey_day"] = pd.to_datetime(
    train_data.Date_of_Journey, format="%d/%m/%Y"
).dt.day
train_data["Journey_month"] = pd.to_datetime(
    train_data["Date_of_Journey"], format="%d/%m/%Y"
).dt.month

# %%
train_data.head()

# %%
# Since we have extracted date and month from Date of journey Coloumn we now don't need Date_of_Journey Column

train_data.drop(["Date_of_Journey"], axis=1, inplace=True)

# %%
# Extracting hour
train_data["Dep_hour"] = pd.to_datetime(train_data["Dep_Time"]).dt.hour

# Extracting minute
train_data["Dep_min"] = pd.to_datetime(train_data["Dep_Time"]).dt.minute

# Since we have extracted hour and minute from Dep_time now we can drop it
train_data.drop(["Dep_Time"], axis=1, inplace=True)


# %%
train_data.head()

# %%
# Similar to above now we can extract hour and minutes from arrival time and finnal drop it.
# Extracting hour
train_data["Arrival_hour"] = pd.to_datetime(train_data["Arrival_Time"]).dt.hour

# Extracting minute
train_data["Arrival_min"] = pd.to_datetime(train_data["Arrival_Time"]).dt.minute

# Since we have extracted hour and minute from Dep_time now we can drop it
train_data.drop(["Arrival_Time"], axis=1, inplace=True)

# %%
train_data.head()

# %%
duration = list(train_data["Duration"])

# Ensure each entry has both hours and minutes in the correct format
for i in range(len(duration)):
    if len(duration[i].split()) != 2:
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"  # Add a space before "0m"
        else:
            duration[i] = "0h " + duration[i]

# Extract hours and minutes
duration_hours = []
duration_mins = []

for i in range(len(duration)):
    # Extract hours and convert to integer
    duration_hours.append(int(duration[i].split(sep="h")[0].strip()))
    # Extract minutes and convert to integer
    duration_mins.append(int(duration[i].split(sep="m")[0].split()[-1].strip()))


# %%
print("Duration:", duration, "\nHours:", duration_hours, "\nMinutes:", duration_mins)


# %%
train_data["Duration_hours"] = duration_hours
train_data["Duration_mins"] = duration_mins
train_data.head()

# %%
train_data.drop(["Duration"], axis=1, inplace=True)
train_data.head()

# %%
train_data["Airline"].value_counts()

# %% [markdown]
# Here The <B>Airline</B> is a catagorical feature. So we perform <B>One Hot Encoding</B>

# %%
# Airlines vs Price
sns.catplot(
    y="Price",
    x="Airline",
    data=train_data.sort_values("Price", ascending=False),
    kind="boxen",
    height=6,
    aspect=3,
)
plt.show()

# %% [markdown]
# ## Analyzing the above Graph
#  From the graph we can see that Jet Airways Business have the highest Price.
#
#  Apart from the Jet Airways Business all the other airways have the similar median.

# %% [markdown]
#

# %%
# One-hot encoding with binary values
Airline = train_data["Airline"]
Airline = pd.get_dummies(Airline, drop_first=True).astype(int)
Airline.head()

# %%
train_data["Source"].value_counts()

# %%
sns.catplot(
    y="Price",
    x="Source",
    data=train_data.sort_values("Price", ascending=False),
    kind="boxen",
    height=6,
    aspect=3,
)
plt.show()


# %%
# As sourse is also a nominal categotry so we will perform one hot Encoding.
Source = train_data[["Source"]]
Source = pd.get_dummies(Source, drop_first=True).astype(int)
Source.head()

# %%
train_data["Destination"].value_counts()


# %%
Destination = train_data[["Destination"]]
Destination = pd.get_dummies(Destination, drop_first=True).astype(int)
Destination.head()

# %%
train_data["Route"]

# %%
# Since additional Infor has almost all the data as no info && The route info can we found out from the number if stops we can drop these datas.
train_data.drop(["Route", "Additional_Info"], axis=1, inplace=True)

# %%
train_data["Total_Stops"].value_counts()

# %%
train_data["Total_Stops"] = train_data["Total_Stops"].replace(
    {"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}
)
train_data.head()

# %%
data_train = pd.concat([train_data, Airline, Source, Destination], axis=1)

# %%
data_train.head()

# %%
data_train.drop(["Airline", "Source", "Destination"], axis=1, inplace=True)

# %%
data_train.head()

# %%
data_train.shape

# %% [markdown]
# Now we perform the exact same steps for test data set.The test data contains the similar data as above but here the price colum is not available as we are trying to fins the predicted price for the test data.

# %%
test_data = pd.read_excel(r"ml/Test_set.xlsx")

# %%
test_data.head()

# %%
test_data.dropna(inplace=True)
test_data["Journey_day"] = pd.to_datetime(
    test_data.Date_of_Journey, format="%d/%m/%Y"
).dt.day
test_data["Journey_month"] = pd.to_datetime(
    test_data["Date_of_Journey"], format="%d/%m/%Y"
).dt.month
# Since we have extracted date and month from Date of journey Coloumn we now don't need Date_of_Journey Column

test_data.drop(["Date_of_Journey"], axis=1, inplace=True)
# Extracting hour
test_data["Dep_hour"] = pd.to_datetime(test_data["Dep_Time"]).dt.hour

# Extracting minute
test_data["Dep_min"] = pd.to_datetime(test_data["Dep_Time"]).dt.minute

# Since we have extracted hour and minute from Dep_time now we can drop it
test_data.drop(["Dep_Time"], axis=1, inplace=True)

# Similar to above now we can extract hour and minutes from arrival time and final drop it.
# Extracting hour
test_data["Arrival_hour"] = pd.to_datetime(test_data["Arrival_Time"]).dt.hour

# Extracting minute
test_data["Arrival_min"] = pd.to_datetime(test_data["Arrival_Time"]).dt.minute

# Since we have extracted hour and minute from Dep_time now we can drop it
test_data.drop(["Arrival_Time"], axis=1, inplace=True)

duration = list(test_data["Duration"])

# Ensure each entry has both hours and minutes in the correct format
for i in range(len(duration)):
    if len(duration[i].split()) != 2:
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"  # Add a space before "0m"
        else:
            duration[i] = "0h " + duration[i]

# Extract hours and minutes
duration_hours = []
duration_mins = []

for i in range(len(duration)):
    # Extract hours and convert to integer
    duration_hours.append(int(duration[i].split(sep="h")[0].strip()))
    # Extract minutes and convert to integer
    duration_mins.append(int(duration[i].split(sep="m")[0].split()[-1].strip()))
print("Duration:", duration, "\nHours:", duration_hours, "\nMinutes:", duration_mins)

test_data["Duration_hours"] = duration_hours
test_data["Duration_mins"] = duration_mins
test_data.head()

test_data.drop(["Duration"], axis=1, inplace=True)
test_data.head()


# One-hot encoding with binary values
Airline = test_data["Airline"]
Airline = pd.get_dummies(Airline, drop_first=True).astype(int)
Airline.head()

Source = test_data[["Source"]]
Source = pd.get_dummies(Source, drop_first=True).astype(int)

Destination = test_data[["Destination"]]
Destination = pd.get_dummies(Destination, drop_first=True).astype(int)

# Since additional Infor has almost all the data as no info && The route info can we found out from the number if stops we can drop these datas.
test_data.drop(["Route", "Additional_Info"], axis=1, inplace=True)

test_data["Total_Stops"] = test_data["Total_Stops"].replace(
    {"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}
)
data_test = pd.concat([test_data, Airline, Source, Destination], axis=1)

data_test.drop(["Airline", "Source", "Destination"], axis=1, inplace=True)


# %%
data_test.head()

# %%
data_test.info()
data_test.shape

# %% [markdown]
# # Feature Selection
# Finding out the best feature which will contribute and have good relation with target variable.Following are some of the feature selection methods,
# <li> heatmap </li>
# <li> feature_importance_ </li>
# <li> SelectKBest </li>

# %%
data_train.shape

# %%
data_train.columns

# %%
X = data_train.loc[
    :,
    [
        "Total_Stops",
        "Journey_day",
        "Journey_month",
        "Dep_hour",
        "Dep_min",
        "Arrival_hour",
        "Arrival_min",
        "Duration_hours",
        "Duration_mins",
        "Air India",
        "GoAir",
        "IndiGo",
        "Jet Airways",
        "Jet Airways Business",
        "Multiple carriers",
        "Multiple carriers Premium economy",
        "SpiceJet",
        "Trujet",
        "Vistara",
        "Vistara Premium economy",
        "Source_Chennai",
        "Source_Delhi",
        "Source_Kolkata",
        "Source_Mumbai",
        "Destination_Cochin",
        "Destination_Delhi",
        "Destination_Hyderabad",
        "Destination_Kolkata",
        "Destination_New Delhi",
    ],
]
X.head()

# %%
y = data_train.iloc[:, 1]
y.head()

# %%
# Finds the correlation between Independent and Dependent attributes

# Filter only numeric columns
numeric_data = train_data.select_dtypes(include=[float, int])

# Plot the heatmap
plt.figure(figsize=(18, 18))
sns.heatmap(numeric_data.corr(), annot=True, cmap="Spectral")
plt.show()


# %%
from sklearn.ensemble import ExtraTreesRegressor

selection = ExtraTreesRegressor()
selection.fit(X, y)

# %%
print(selection.feature_importances_)

# %%
# plot graph of feature importances for better visualization

plt.figure(figsize=(12, 8))
feat_importances = pd.Series(selection.feature_importances_, index=X.columns)
feat_importances.nlargest(20).plot(kind="barh")
plt.show()


# %% [markdown]
# ---

# %% [markdown]
# ## Fitting model using Random Forest
#
# 1. Split dataset into train and test set in order to prediction w.r.t X_test
# 2. If needed do scaling of data
#     * Scaling is not done in Random forest
# 3. Import model
# 4. Fit the data
# 5. Predict w.r.t X_test
# 6. In regression check **RSME** Score
# 7. Plot graph

# %%
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# %%
from sklearn.ensemble import RandomForestRegressor

reg_rf = RandomForestRegressor()
reg_rf.fit(X_train, y_train)

# %%
y_pred = reg_rf.predict(X_test)

# %%
reg_rf.score(X_train, y_train)

# %%
reg_rf.score(X_test, y_test)

# %%
sns.histplot(y_test - y_pred)
plt.show()

# %%

plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("y_test")
plt.ylabel("y_pred")
plt.show()

# %%
from sklearn import metrics

# %%
print("MAE:", metrics.mean_absolute_error(y_test, y_pred))
print("MSE:", metrics.mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

# %%
# RMSE/(max(DV)-min(DV))

2090.5509 / (max(y) - min(y))

# %%
metrics.r2_score(y_test, y_pred)

# %% [markdown]
# ---

# %% [markdown]
# ## Hyperparameter Tuning
#
#
# * Choose following method for hyperparameter tuning
#     1. **RandomizedSearchCV** --> Fast
#     2. **GridSearchCV**
# * Assign hyperparameters in form of dictionery
# * Fit the model
# * Check best paramters and best score

# %%
from sklearn.model_selection import RandomizedSearchCV

reg_rf = RandomForestRegressor()

# %%
# Randomized Search CV

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start=100, stop=1200, num=12)]

# Number of features to consider at every split
max_features = ["sqrt", "log2"]  # Replace 'auto' with 'sqrt' or 'log2'

# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num=6)]

# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10, 15, 100]

# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 5, 10]

# %%
# Create the random grid

random_grid = {
    "n_estimators": n_estimators,
    "max_features": max_features,
    "max_depth": max_depth,
    "min_samples_split": min_samples_split,
    "min_samples_leaf": min_samples_leaf,
}

# %%
# Random search of parameters, using 5 fold cross validation,
# search across 100 different combinations
rf_random = RandomizedSearchCV(
    estimator=reg_rf,
    param_distributions=random_grid,
    scoring="neg_mean_squared_error",
    n_iter=10,
    cv=5,
    verbose=2,
    random_state=42,
    n_jobs=-1,
)

# %%
X_train = X_train.fillna(X_train.mean())  # Impute NaNs in X_train
y_train = y_train.fillna(y_train.mean())  # Impute NaNs in y_train

# Check for infinite values and replace with NaN
X_train.replace([np.inf, -np.inf], np.nan, inplace=True)
X_train = X_train.fillna(X_train.mean())

# %%
print(X_train.dtypes)

# %%
rf_random.fit(X_train, y_train)

# %%
rf_random.best_params_

# %%
prediction = rf_random.predict(X_test)

# %%
import seaborn as sns

plt.figure(figsize=(8, 8))
sns.histplotplot(y_test - prediction)
plt.show()


# %%
plt.figure(figsize=(8, 8))
plt.scatter(y_test, prediction, alpha=0.5)
plt.xlabel("y_test")
plt.ylabel("y_pred")
plt.show()

# %% [markdown]
# ---

# %% [markdown]
# ## Saving the model to reuse it again

# %%
import pickle

# Save the best model (the model after hyperparameter tuning)
with open("flight_price_rf.pkl", "wb") as file:
    pickle.dump(rf_random.best_estimator_, file)
print("Best Parameters:", rf_random.best_params_)

# %% [markdown]
# # Loading and Predicting Using the Saved Model:

# %%
# Load the saved best model
with open("flight_price_rf.pkl", "rb") as file:
    forest = pickle.load(file)

# Make predictions using the loaded model
y_prediction = forest.predict(X_test)

# Evaluate the model's performance
from sklearn import metrics

print("MAE:", metrics.mean_absolute_error(y_test, y_prediction))
print("MSE:", metrics.mean_squared_error(y_test, y_prediction))
print("RMSE:", np.sqrt(metrics.mean_squared_error(y_test, y_prediction)))


# %%
metrics.r2_score(y_test, y_prediction)

# %% predict Price
sample_input = np.array(
    [
        1,
        12,
        5,
        18,
        5,
        23,
        30,
        5,
        25,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        11,
    ]
)
predicted_price = forest.predict(sample_input)
print("Predicted Price:", predicted_price[0])
