# Importing Dependencies
import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

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
df['Target_Direction'] = (df['Close'].shift(-1) > df['Close']).astype(int)

#Droping the very last row because we don't know tomorrow's price for today yet.
df = df.dropna()

# 3. Defining thefetures and targets for model to look into.
# Features/X = What the model is allowed to look at.
features = ['Close','SMA_50','Volatility','RSI','MACD','MACD_Histogram']
X = df[features]

# Target/Y = What the model is trying to guess.
Y = df['Target_Direction']

# 4. Train-Test Split
# We divide the data into training set and testing set.
# Training (80% of data) is used to teach the model so it can learn.
# Remainig (20% of data) is used for testing on the accuracy of it's learning.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=False)

# 5. Performing training on the model.
print("Training Random Forest Classifier....")
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, Y_train)

# 6. Checking the learning of the model.
# Leting the model guess the prices for the remaining 20% of the data which was never introduced to it.
predictions = model.predict(X_test)

# Calculating the mean absolute error (Showing how many rupees off it is on average.)
accuracy = accuracy_score(Y_test,predictions)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(Y_test, predictions))
