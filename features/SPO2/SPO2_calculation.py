import numpy as np
from scipy.signal import find_peaks

def calculate_spo2(file_path):
    # Initialize an empty list to hold valid numeric data
    valid_data = []

    # Open and read the file, ignoring non-numeric lines
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Try to convert each line into a list of floats
                parts = list(map(float, line.strip().split(',')))
                if len(parts) == 3:  # Ensure the line has exactly three values (for three sensors)
                    valid_data.append(parts)
            except ValueError:
                # Skip lines that contain non-numeric values
                continue

    # Convert the valid data into a numpy array
    data = np.array(valid_data)

    # Ensure that the data has at least two columns
    if data.shape[1] < 2:
        return "Error: Insufficient data for SpO2 calculation."

    # Separating data for each sensor
    sensor1_data = data[:, 0]  # Red light sensor
    sensor2_data = data[:, 1]  # Infrared (IR) light sensor

    # Detecting peaks and troughs
    def detect_peaks_troughs(sensor_data):
        peaks, _ = find_peaks(sensor_data)
        troughs, _ = find_peaks(-sensor_data)
        return peaks, troughs

    peaks_sensor1, troughs_sensor1 = detect_peaks_troughs(sensor1_data)
    peaks_sensor2, troughs_sensor2 = detect_peaks_troughs(sensor2_data)

    # Ensure the number of peaks and troughs are the same for correct pairing
    def adjust_peaks_troughs(peaks, troughs):
        if len(peaks) > len(troughs):
            peaks = peaks[:len(troughs)]
        elif len(troughs) > len(peaks):
            troughs = troughs[:len(peaks)]
        return peaks, troughs

    peaks_sensor1, troughs_sensor1 = adjust_peaks_troughs(peaks_sensor1, troughs_sensor1)
    peaks_sensor2, troughs_sensor2 = adjust_peaks_troughs(peaks_sensor2, troughs_sensor2)

    # Calculate AC and DC components
    def calculate_ac_dc(signal, peaks, troughs):
        ac_values = signal[peaks] - signal[troughs]
        dc_values = (signal[peaks] + signal[troughs]) / 2
        return ac_values, dc_values

    ac_sensor1, dc_sensor1 = calculate_ac_dc(sensor1_data, peaks_sensor1, troughs_sensor1)
    ac_sensor2, dc_sensor2 = calculate_ac_dc(sensor2_data, peaks_sensor2, troughs_sensor2)

    # Adjust the lengths of the AC/DC values to be the same
    min_length = min(len(ac_sensor1), len(ac_sensor2))

    ac_sensor1 = ac_sensor1[:min_length]
    dc_sensor1 = dc_sensor1[:min_length]
    ac_sensor2 = ac_sensor2[:min_length]
    dc_sensor2 = dc_sensor2[:min_length]

    # Calculate Ratio of Ratios (R)
    ratio_red = ac_sensor1 / dc_sensor1
    ratio_ir = ac_sensor2 / dc_sensor2
    R = ratio_red / ratio_ir

    # Calibration coefficients A and B
    A = 96.47017376615973
    B = -0.35285299637920736

    # Calculate SpO2
    SpO2 = A - (B * R)
    final_spo2 = np.mean(SpO2)

    return final_spo2
