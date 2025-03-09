import numpy as np
from scipy.signal import cwt, ricker, find_peaks

def estimate_heart_rate(file_path, scale=10, sample_rate=100, peak_distance=50):
    # Initialize a list to hold valid numeric data from the third column
    valid_data = []

    # Open and read the file, ignoring lines with insufficient columns
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Try to read the third column (index 2) from the comma-separated values
                parts = line.strip().split(',')
                if len(parts) >= 3:  # Ensure the line has at least three columns
                    valid_data.append(float(parts[2]))  # Use the third column (index 2)
            except ValueError:
                # Skip lines that contain non-numeric values
                continue

    # Convert the valid data into a numpy array
    data = np.array(valid_data)

    # Check if there's sufficient data to process
    if len(data) == 0:
        return "Error: No valid data available for processing."

    # Apply Continuous Wavelet Transform (CWT)
    widths = np.arange(1, 50)
    cwtmatr = cwt(data, ricker, widths)

    # Check if the scale is within range of cwtmatr dimensions
    if scale >= cwtmatr.shape[0]:
        return f"Error: Requested scale {scale} exceeds available scales {cwtmatr.shape[0]}."

    # Analyze a specific scale that corresponds to the expected heart rate frequency
    ridge_data = cwtmatr[scale, :]

    # Detect peaks in the ridge data
    peaks, _ = find_peaks(ridge_data, distance=peak_distance)

    if len(peaks) == 0:
        return "Error: No peaks detected in the data, unable to calculate heart rate."

    # Calculate heart rate
    duration_seconds = len(data) / sample_rate
    heart_rate = len(peaks) * (60 / duration_seconds)

    # Plotting the results (optional, currently disabled)
    # plt.figure(figsize=(10, 4))
    # plt.plot(ridge_data, label='Wavelet Transformed Data')
    # plt.plot(peaks, ridge_data[peaks], "x", label='Detected Peaks')
    # plt.title('Heart Rate Detection using CWT')
    # plt.xlabel('Samples')
    # plt.ylabel('CWT Coefficient')
    # plt.legend()
    # plt.show()

    return heart_rate
