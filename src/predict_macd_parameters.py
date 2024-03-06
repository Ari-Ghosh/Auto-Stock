import torch

def predict_macd_parameters(model, new_data):
    new_data_tensor = torch.tensor(new_data.values, dtype=torch.float32)
    model.eval()
    with torch.no_grad():
        predicted_params = model(new_data_tensor)
    return predicted_params.numpy()