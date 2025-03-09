def calculate_temperature(file_path):
    """
    Calculate the average temperature from a file containing IR intensity data.
    The slope and intercept for the temperature calculation are hardcoded.

    Parameters:
    - file_path: Path to the input file containing comma-separated data.

    Returns:
    - Average temperature calculated from the data or None if no valid data is found.
    """
    temperatures = []

    # Hardcoded slope and intercept
    slope = -4.589088663112415e-05
    intercept = 37.44431836475507

    # Open and process the file
    # Open and process the file
    with open(file_path, 'r') as file:
        for line in file:
            try:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    ir_intensity = int(parts[1])  # Use the second column for IR
                    temperature = slope * ir_intensity + intercept
                    temperatures.append(temperature)
            except ValueError:
                continue
    
    # Calculate the average temperature if data is present
    if temperatures:
        average_temperature = sum(temperatures) / len(temperatures)
        return average_temperature
    else:
        return None

# Example usage:
# file_path = 'ayush_bp_100_64.txt'  # Adjust the file path as needed

# # Calculate the average temperature
# average_temperature = calculate_temperature(file_path)

# # Output the result
# if average_temperature is not None:
#     print(f"The average temperature is: {average_temperature:.2f} °C")
# else:
#     print("No temperature data found.")
