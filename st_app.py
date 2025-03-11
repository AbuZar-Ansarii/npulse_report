import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt
import io # Import io for in-memory file handling

# Import your feature functions
# Assuming these are in your project structure:
from features.Nadi.functions_script import *
from features.Nadi.signal_process import *
from features.Nadi.nadi_processor_double import process_nadi_data_double
from features.Nadi.nadi_processor import process_nadi_data
from features.BP.predict_bp import predict_bp
from features.HeartRate.hr_calculation import estimate_heart_rate
from features.Temperature.TEMP_calculation import calculate_temperature
from features.SPO2.SPO2_calculation import calculate_spo2
from nadi_report.report_generation import create_comprehensive_pdf

# Setup logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app_terminal.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


# Allowed file extension for our text files
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "txt"


# Download file if a URL is provided
def download_file(url, dest_folder="tempFiles"):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    response = requests.get(url)
    if response.status_code != 200:
        logger.error("Failed to download file from URL")
        raise Exception("Failed to download file from URL")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = os.path.join(dest_folder, f"temp_file_{timestamp}.txt")
    with open(temp_path, "wb") as f:
        f.write(response.content)
    return temp_path


def get_health_metrics(file_source):
    try:
        if isinstance(file_source, str) and (
            file_source.startswith("http://") or file_source.startswith("https://")
        ):
            file_path = download_file(file_source)
        else:
            # Handle uploaded file directly as bytes
            file_path = io.BytesIO(file_source.getvalue())

        data = {}

        try:
            systolic_bp, diastolic_bp = predict_bp(file_path)
            data["systolic_bp"] = systolic_bp
            data["diastolic_bp"] = diastolic_bp
        except Exception as e:
            logger.error(f"Error in predict_bp: {e}")
            raise Exception(f"Error in BP prediction: {e}")

        try:
            heart_rate = estimate_heart_rate(file_path)
            data["heart_rate"] = heart_rate
        except Exception as e:
            logger.error(f"Error in estimate_heart_rate: {e}")
            raise Exception(f"Error in heart rate calculation: {e}")

        try:
            temperature = calculate_temperature(file_path)
            data["temperature"] = temperature
        except Exception as e:
            logger.error(f"Error in calculate_temperature: {e}")
            raise Exception(f"Error in temperature calculation: {e}")

        try:
            spo2 = calculate_spo2(file_path)
            data["spo2"] = spo2
        except Exception as e:
            logger.error(f"Error in calculate_spo2: {e}")
            raise Exception(f"Error in SpO2 calculation: {e}")

        return data

    except Exception as e:
        logger.error(f"Error in get_health_metrics: {e}")
        st.error(f"Error: {e}")
        return None



# Function to load data from a file-like object
def load_data_from_file(file):
    data = []
    file.seek(0)
    try:
        for line in file:
            line = line.decode("utf-8").strip()
            if line:
                parts = line.split(",")
                if len(parts) != 3:
                    continue
                try:
                    numbers = list(map(float, parts))
                    data.append(numbers)
                except ValueError:
                    st.warning(f"Error converting line to numbers: {line}")
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return data


# Function to trim the data
def trim_data(data):
    return data[len(data) // 2 :] if len(data) > 1 else data


# Function to visualize the heart rate data
def visualize_data(data):
    if not data:
        st.error("No valid data to visualize.")
        return

    trimmed_data = trim_data(data)

    x = list(range(1, len(trimmed_data) + 1))
    col1 = [row[0] for row in trimmed_data]
    col2 = [row[1] for row in trimmed_data]
    col3 = [row[2] for row in trimmed_data]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, col1, label="Data Series 1", linewidth=1.5)
    ax.plot(x, col2, label="Data Series 2", linewidth=1.5)
    ax.plot(x, col3, label="Data Series 3", linewidth=1.5)

    ax.set_title("Heart Rate Data Visualization")
    ax.set_xlabel("Measurement Index")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)


# Function to visualize data from a file
def visualize_heart_rate_data(file):
    data = load_data_from_file(file)
    if data:
        visualize_data(data)

def main():
    st.title("N-PULSE DATA PROCESSING")
    st.sidebar.title("N-PULSE")
    uploaded_file = st.sidebar.file_uploader("Upload Data file", type="txt")
    if uploaded_file:
        if st.sidebar.button("Process"):
            st.header("HEALTH METRICS")
            try:
                metrics = get_health_metrics(uploaded_file)
                if metrics:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.header("Heart Rate")
                        st.header(int(metrics.get("heart_rate", "N/A")))
                    with col2:
                        st.header("Temperature")
                        st.header(int(metrics.get("temperature", "N/A")))
                    with col3:
                        st.header("SpO2")
                        st.header(int(metrics.get("spo2", "N/A")))
                    col4, col5 = st.columns(2)
                    with col4:
                        st.header("Diastolic BP")
                        st.header(int(metrics.get("diastolic_bp", "N/A")))
                    with col5:
                        st.header("Systolic BP")
                        st.header(int(metrics.get("systolic_bp", "N/A")))

                    st.header("DATA VISUALIZATION")
                    visualize_heart_rate_data(uploaded_file)
                else:
                    st.error("Failed to retrieve health metrics.")
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
