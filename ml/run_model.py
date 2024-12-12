import pickle
import numpy as np
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
with open("ml/flight_price_rf.pkl", "rb") as file:
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
