import torch
import torch.nn as nn
import torch.optim as optim
from model import MACDModel

def train_macd_parameters(features, targets):
    input_size = features.shape[1]
    hidden_size1, hidden_size2 = 64, 32
    output_size = 3  # MACD parameters: fast, slow, smooth

    model = MACDModel(input_size, hidden_size1, hidden_size2, output_size)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    features_tensor = torch.tensor(features.values, dtype=torch.float32)
    targets_tensor = torch.tensor(targets.values, dtype=torch.float32)

    num_epochs = 50
    for epoch in range(num_epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(features_tensor)
        loss = criterion(outputs, targets_tensor)
        loss.backward()
        optimizer.step()

    return model