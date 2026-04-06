# Importing Dependencies
import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. Connect to the cloud vault
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

symbol = "RELIANCE.NS"
query = f'SELECT * FROM "{symbol}"'
df = pd.read_sql_query(query, engine, index_col='Date', parse_dates=['Date'])

print(f"Loaded {len(df)} days of data for {symbol}.")

# 2. The Machine Learning Shift (Creating Target)
# Shifting the close column UP by 1 for setting the target.
df['Target_Tomorrow_Close'] = df['Close'].shift(-1)

#Droping the very last row because we don't know tomorrow's price for today yet.
df = df.dropna()

# 3. Defining thefetures and targets for model to look into.
# Features/X = What the model is allowed to look at.
features = ['Close','SMA_50','Volatility','RSI','MACD','MACD_Histogram']
X = df[features]

# Target/Y = What the model is trying to guess.
Y = df['Target_Tomorrow_Close']

# 4. Train-Test Split
# We divide the data into training set and testing set.
# Training (80% of data) is used to teach the model so it can learn.
# Remainig (20% of data) is used for testing on the accuracy of it's learning.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=False)

# 5. Performing training on the model.
print("Training Random Forest Regressor....")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, Y_train)

# 6. Checking the learning of the model.
# Leting the model guess the prices for the remaining 20% of the data which was never introduced to it.
predictions = model.predict(X_test)

# Calculating the mean absolute error (Showing how many rupees off it is on average.)
mae = mean_absolute_error(Y_test,predictions)
print(f"Mean Absolute Error (MAE): ₹{mae:.2f}")

# 7. Visualizing the Brain.
# Ploting the actual historical prices vs the algorithm's predictions
plt.figure(figsize=(12,6))
plt.plot(Y_test.index, Y_test.values, label='Actual Price', color='blue')
plt.plot(Y_test.index, predictions, label='Predicted Price', color='red', linestyle='dashed')
plt.title(f"{symbol}: Actual vs Predicted Price (Test Data)")
plt.legend()
plt.show()