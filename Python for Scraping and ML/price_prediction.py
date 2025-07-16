import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

data = pd.read_csv('hotel_prices_cleaned.csv')

# Encode dates as numbers
data['Check-in'] = pd.to_datetime(data['Check-in']
                                  ).map(lambda d: d.toordinal())
data['Check-out'] = pd.to_datetime(data['Check-out']
                                   ).map(lambda d: d.toordinal())

# Build hotel name mapping
hotel_names = sorted(data['Hotel Name'].unique())
hotel_to_index = {name: idx for idx, name in enumerate(hotel_names)}
index_to_hotel = {idx: name for name, idx in hotel_to_index.items()}

# Encode hotel names as integers
data['Hotel_Index'] = data['Hotel Name'].map(hotel_to_index)

# Features and targets
X = data[['Hotel_Index', 'Check-in', 'Check-out']].values
y = data['Price'].values.reshape(-1, 1)

# Normalize features
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_norm = (X - X_mean) / X_std

X_tensor = torch.tensor(X_norm, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.float32)


# Define Model : Neural Network
model = nn.Sequential(
    nn.Linear(X_tensor.shape[1], 64),
    nn.ReLU(),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, 1)
)

loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)


# Train Model
print("Training model...")
for epoch in range(200):
    optimizer.zero_grad()
    pred = model(X_tensor)
    loss = loss_fn(pred, y_tensor)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.2f}")

print("Training complete!\n")


# Predict Function

def predict_price(hotel_name, checkin_date, checkout_date):
    hotel_idx = hotel_to_index.get(hotel_name)
    if hotel_idx is None:
        raise ValueError(f"Unknown hotel name: {hotel_name}")

    checkin_ord = pd.to_datetime(checkin_date).toordinal()
    checkout_ord = pd.to_datetime(checkout_date).toordinal()

    features = np.array([[hotel_idx, checkin_ord, checkout_ord]])
    features_norm = (features - X_mean) / X_std

    features_tensor = torch.tensor(features_norm, dtype=torch.float32)
    prediction = model(features_tensor).item()
    return prediction


# Prediction Choice
new_price = predict_price(
    hotel_name="Hilton Taipei Sinban",
    checkin_date="2025-09-21",
    checkout_date="2025-09-22"
)

print(f" Predicted price for new date: TWD {new_price:.0f}")
