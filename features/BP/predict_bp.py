import joblib
import numpy as np
from scipy.signal import find_peaks
import os

# Define the function to extract features and predict BP
def predict_bp(file_path):
    # Initialize lists to store the data
    red_signals = []
    ir_signals = []
    green_signals = []

    # Read the file and split the data
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Only process lines with three comma-separated values
                parts = line.strip().split(',')
                if len(parts) == 3:
                    red, ir, green = map(int, parts)
                    red_signals.append(red)
                    ir_signals.append(ir)
                    green_signals.append(green)
            except ValueError:
                # Skip lines that cannot be parsed into integers
                continue

    # Feature extraction function
    def extract_features(red_signal, ir_signal, green_signal):
        peaks_red, _ = find_peaks(red_signal, distance=50)
        peaks_ir, _ = find_peaks(ir_signal, distance=50)
        
        # Ensure peaks_red and peaks_ir have the same length
        min_length = min(len(peaks_red), len(peaks_ir))
        peaks_red = peaks_red[:min_length]
        peaks_ir = peaks_ir[:min_length]
        
        # PTT - pulse transit time
        ptt = np.mean(np.diff(peaks_ir) - np.diff(peaks_red))
        
        features = {
            'mean_red': np.mean(red_signal),
            'std_red': np.std(red_signal),
            'mean_ir': np.mean(ir_signal),
            'std_ir': np.std(ir_signal),
            'mean_green': np.mean(green_signal),
            'std_green': np.std(green_signal),
            'ptt': ptt
        }
        return features

    # Extract features from the signals
    efeatures = extract_features(red_signals, green_signals, ir_signals)

    # Assign feature values
    Red_Average = efeatures['mean_red']
    Green_Average = efeatures['mean_green']
    IR_Average = efeatures['mean_ir']
    Red_STD = efeatures['std_red']
    Green_STD = efeatures['std_green']
    IR_STD = efeatures['std_ir']
    PTT = efeatures['ptt']

    # Correct the paths to model and scaler files
    model_path = os.path.join(os.getcwd(), 'features', 'BP', 'svr_model.pkl')
    scaler_X_path = os.path.join(os.getcwd(), 'features', 'BP', 'scaler_X.pkl')
    scaler_y_path = os.path.join(os.getcwd(), 'features', 'BP', 'scaler_y.pkl')

    # Load the saved model and scalers
    model = joblib.load(model_path)
    scaler_X = joblib.load(scaler_X_path)
    scaler_y = joblib.load(scaler_y_path)

    # Use a new test input (as a new row with similar features as your training data)
    new_test_input = [[Red_Average, Green_Average, IR_Average, Red_STD, Green_STD, IR_STD, PTT]]  # Example input

    # Normalize the new test input
    new_test_input_scaled = scaler_X.transform(new_test_input)

    # Make predictions
    predicted_scaled = model.predict(new_test_input_scaled)
    predicted = scaler_y.inverse_transform(predicted_scaled)

    # Return the predicted Systolic and Diastolic blood pressure values
    systolic_bp = predicted[0][0]
    diastolic_bp = predicted[0][1]
    return systolic_bp, diastolic_bp
