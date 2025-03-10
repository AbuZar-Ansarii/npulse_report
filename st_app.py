# import json
# import logging
# import threading
# import time
# from datetime import datetime

# import pandas as pd
# import requests
# import streamlit as st
# import matplotlib.pyplot as plt

# # Import your feature functions
# from features.Nadi.functions_script import *
# from features.Nadi.signal_process import *
# from features.Nadi.nadi_processor_double import process_nadi_data_double
# from features.Nadi.nadi_processor import process_nadi_data
# from features.BP.predict_bp import predict_bp
# from features.HeartRate.hr_calculation import estimate_heart_rate
# from features.Temperature.TEMP_calculation import calculate_temperature
# from features.SPO2.SPO2_calculation import calculate_spo2
# from nadi_report.report_generation import create_comprehensive_pdf  # Import your PDF generation function

# # Setup logging
# logging.basicConfig(
#     level=logging.ERROR,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler("app_terminal.log"),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)


# def fetch_url(url):
#     """Fetch content from a given URL."""
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.text
#     except Exception as e:
#         print(f"Error fetching URL: {e}")
#         return None


# # Allowed file extension for our text files
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'


# # Download file if a URL is provided
# def download_file(url, dest_folder="tempFiles"):
#     if not os.path.exists(dest_folder):
#         os.makedirs(dest_folder)
#     response = requests.get(url)
#     if response.status_code != 200:
#         logger.error("Failed to download file from URL")
#         raise Exception("Failed to download file from URL")
#     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#     temp_path = os.path.join(dest_folder, f'temp_file_{timestamp}.txt')
#     with open(temp_path, 'wb') as f:
#         f.write(response.content)
#     return temp_path


# # Delete temporary file after delay
# def delete_file_after_delay(file_path, delay=60):
#     def delete_file():
#         time.sleep(delay)
#         if os.path.exists(file_path):
#             os.remove(file_path)
#             print(f"{file_path} has been deleted from the system.")

#     threading.Thread(target=delete_file).start()


# # Mode 1: Process Nadi Data (single file)
# def process_nadi(file_source, hand):
#     try:
#         if file_source.startswith("http://") or file_source.startswith("https://"):
#             file_path = download_file(file_source)
#             temp_download = True
#         else:
#             file_path = file_source
#             temp_download = False

#         if not allowed_file(file_path):
#             raise Exception("Invalid file type. Only '.txt' files are allowed.")

#         # Process Nadi data
#         result = process_nadi_data(file_path, hand)
#         st.json(result)

#         # Add download button for the result
#         result_str = json.dumps(result, indent=4)
#         st.download_button(
#             label="Download Nadi Data Result",
#             data=result_str,
#             file_name="nadi_data_result.json",
#             mime="application/json"
#         )

#     except Exception as e:
#         logger.error(f"Error in process_nadi: {e}")
#         st.error(f"Error: {e}")
#     finally:
#         if temp_download and os.path.exists(file_path):
#             os.remove(file_path)


# # Mode 2: Process Double Nadi Data (two files)
# def process_nadi_double(file_source1, file_source2, hand):
#     temp_files = []
#     try:
#         # Process first file
#         if file_source1.startswith("http://") or file_source1.startswith("https://"):
#             file_path1 = download_file(file_source1)
#             temp_files.append(file_path1)
#         else:
#             file_path1 = file_source1

#         # Process second file
#         if file_source2.startswith("http://") or file_source2.startswith("https://"):
#             file_path2 = download_file(file_source2)
#             temp_files.append(file_path2)
#         else:
#             file_path2 = file_source2

#         if not (allowed_file(file_path1) and allowed_file(file_path2)):
#             raise Exception("Invalid file type for one or both files. Only '.txt' files are allowed.")

#         # Process double Nadi data
#         result = process_nadi_data_double(file_path1, file_path2, hand)
#         st.json(result)

#         # Add download button for the result
#         result_str = json.dumps(result, indent=4)
#         st.download_button(
#             label="Download Double Nadi Data Result",
#             data=result_str,
#             file_name="double_nadi_data_result.json",
#             mime="application/json"
#         )

#     except Exception as e:
#         logger.error(f"Error in process_nadi_double: {e}")
#         st.error(f"Error: {e}")
#     finally:
#         for fp in temp_files:
#             if os.path.exists(fp):
#                 os.remove(fp)


# # Mode 3: Get Health Metrics
# def get_health_metrics(file_source):
#     temp_download = False
#     try:
#         if file_source.startswith("http://") or file_source.startswith("https://"):
#             file_path = download_file(file_source)
#             temp_download = True
#         else:
#             file_path = file_source

#         if not allowed_file(file_path):
#             raise Exception("Invalid file type. Only '.txt' files are allowed.")

#         data = {}

#         try:
#             systolic_bp, diastolic_bp = predict_bp(file_path)
#             data['systolic_bp'] = systolic_bp
#             data['diastolic_bp'] = diastolic_bp
#         except Exception as e:
#             logger.error(f"Error in predict_bp: {e}")
#             raise Exception(f"Error in BP prediction: {e}")

#         try:
#             heart_rate = estimate_heart_rate(file_path)
#             data['heart_rate'] = heart_rate
#         except Exception as e:
#             logger.error(f"Error in estimate_heart_rate: {e}")
#             raise Exception(f"Error in heart rate calculation: {e}")

#         try:
#             temperature = calculate_temperature(file_path)
#             data['temperature'] = temperature
#         except Exception as e:
#             logger.error(f"Error in calculate_temperature: {e}")
#             raise Exception(f"Error in temperature calculation: {e}")

#         try:
#             spo2 = calculate_spo2(file_path)
#             data['spo2'] = spo2
#         except Exception as e:
#             logger.error(f"Error in calculate_spo2: {e}")
#             raise Exception(f"Error in SpO2 calculation: {e}")

#         st.json(data)

#         # Add download button for the result
#         result_str = json.dumps(data, indent=4)
#         st.download_button(
#             label="Download Health Metrics Result",
#             data=result_str,
#             file_name="health_metrics_result.json",
#             mime="application/json"
#         )

#     except Exception as e:
#         logger.error(f"Error in get_health_metrics: {e}")
#         st.error(f"Error: {e}")
#     finally:
#         if temp_download and os.path.exists(file_path):
#             os.remove(file_path)


# # Mode 4: Generate Comprehensive Nadi Report
# def generate_report(json_input_path):
#     try:
#         with open(json_input_path, 'r') as f:
#             data = json.load(f)

#         required_keys = [
#             "hand", "nadiFileUrl", "patient_data", "doctor_data",
#             "dosha_analysis", "vital_signs_data", "food_data_json", "yoga_data", "routine_data"
#         ]
#         missing_keys = [key for key in required_keys if key not in data]
#         if missing_keys:
#             raise Exception(f"Missing required data in JSON: {', '.join(missing_keys)}")

#         # Get nadi file from URL or file path
#         nadi_source = data["nadiFileUrl"]
#         if nadi_source.startswith("http://") or nadi_source.startswith("https://"):
#             nadi_file_path = download_file(nadi_source)
#             temp_download = True
#         else:
#             nadi_file_path = nadi_source
#             temp_download = False

#         if not allowed_file(nadi_file_path):
#             raise Exception("Invalid nadi file type. Only '.txt' files are allowed.")

#         # Process Nadi data
#         hand = data["hand"]
#         nadi_response = process_nadi_data(nadi_file_path, hand)
#         chart_data1 = nadi_response.get("single_beat_data", {})
#         input_data = nadi_response.get("processed_data", {})

#         # Format processed data for report
#         nadi_check_data = {
#             "Kapha": {
#                 "HR": input_data.get('a_HR', [None])[0],
#                 "HRV": input_data.get('a_HRV', [None])[0],
#                 "PV": input_data.get('a_auc', [None])[0],
#                 "PA": input_data.get('a_amp', [None])[0],
#                 "MST": input_data.get('a_st', [None])[0]
#             },
#             "Pitta": {
#                 "HR": input_data.get('a_HR', [None, None])[1],
#                 "HRV": input_data.get('a_HRV', [None, None])[1],
#                 "PV": input_data.get('a_auc', [None, None])[1],
#                 "PA": input_data.get('a_amp', [None, None])[1],
#                 "MST": input_data.get('a_st', [None, None])[1]
#             },
#             "Vatta": {
#                 "HR": input_data.get('a_HR', [None, None, None])[2],
#                 "HRV": input_data.get('a_HRV', [None, None, None])[2],
#                 "PV": input_data.get('a_auc', [None, None, None])[2],
#                 "PA": input_data.get('a_amp', [None, None, None])[2],
#                 "MST": input_data.get('a_st', [None, None, None])[2]
#             }
#         }

#         # Generate PDF filename and path
#         patient_data = data["patient_data"]
#         patient_name = patient_data.get('name', 'Unknown_Patient').split()[0]
#         reports_dir = 'reports'
#         if not os.path.exists(reports_dir):
#             os.makedirs(reports_dir)
#         timestamp = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
#         pdf_filename = f"dosha_report_{patient_name}_{timestamp}.pdf"
#         pdf_filepath = os.path.join(reports_dir, pdf_filename)

#         # Generate PDF report
#         create_comprehensive_pdf(
#             filename=pdf_filepath,
#             patient_data=data["patient_data"],
#             doctor_data=data["doctor_data"],
#             vital_signs=data.get("vital_signs", {}),  # Default empty dictionary if missing
#             dosha_analysis=data["dosha_analysis"],
#             vital_signs_data=data["vital_signs_data"],
#             nadi_check_data=nadi_check_data,
#             chart_data1=chart_data1,
#             food_data_json=data["food_data_json"],
#             yoga_data=data["yoga_data"],
#             routine_data=data["routine_data"]
#         )

#         st.success(f"Report generated successfully: {pdf_filepath}")

#         # Add download button for the generated PDF
#         with open(pdf_filepath, "rb") as f:
#             st.download_button(
#                 label="Download Comprehensive Nadi Report",
#                 data=f,
#                 file_name=pdf_filename,
#                 mime="application/pdf"
#             )

#     except Exception as e:
#         logger.error(f"Error in generate_report: {e}")
#         st.error(f"Error: {e}")
#     finally:
#         # Clean up temporary nadi file if downloaded
#         if 'temp_download' in locals() and temp_download and os.path.exists(nadi_file_path):
#             os.remove(nadi_file_path)


# # Mode 5: Visualize Heart Rate Data
# # Function to load data from a file
# def load_data_from_file(filename):
#     data = []
#     try:
#         with open(filename, 'r') as file:
#             for line in file:
#                 line = line.strip()
#                 if line:
#                     parts = line.split(',')
#                     if len(parts) != 3:
#                         st.warning(f"Skipping line (unexpected format): {line}")
#                         continue
#                     try:
#                         numbers = list(map(float, parts))
#                         data.append(numbers)
#                     except ValueError:
#                         st.warning(f"Error converting line to numbers: {line}")
#     except FileNotFoundError:
#         st.error(f"File not found: {filename}")
#     return data

# # Function to trim the data
# def trim_data(data):
#     """Trim the data by taking only the latter half of the data points."""
#     return data[len(data) // 2:] if len(data) > 1 else data

# # Function to visualize the heart rate data
# def visualize_data(data):
#     if not data:
#         st.error("No valid data to visualize.")
#         return

#     trimmed_data = trim_data(data)

#     x = list(range(1, len(trimmed_data) + 1))
#     col1 = [row[0] for row in trimmed_data]
#     col2 = [row[1] for row in trimmed_data]
#     col3 = [row[2] for row in trimmed_data]

#     fig, ax = plt.subplots(figsize=(12, 6))
#     ax.plot(x, col1, label='Data Series 1', linewidth=1.5)
#     ax.plot(x, col2, label='Data Series 2', linewidth=1.5)
#     ax.plot(x, col3, label='Data Series 3', linewidth=1.5)

#     ax.set_title('Heart Rate Data Visualization')
#     ax.set_xlabel('Measurement Index')
#     ax.set_ylabel('Value')
#     ax.legend()
#     ax.grid(True)
#     plt.tight_layout()
#     st.pyplot(fig)

# # Function to visualize data from a file
# def visualize_heart_rate_data(filename):
#     data = load_data_from_file(filename)
#     if data:
#         visualize_data(data)

# # Function to visualize data from a URL
# def url_visualize_heart_rate_data(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         lines = response.text.splitlines()
#     except requests.RequestException as e:
#         st.error(f"Error fetching data: {e}")
#         return

#     data = []
#     for line in lines:
#         line = line.strip()
#         if line:
#             parts = line.split(',')
#             if len(parts) != 3:
#                 st.warning(f"Skipping line (unexpected format): {line}")
#                 continue
#             try:
#                 numbers = list(map(float, parts))
#                 data.append(numbers)
#             except ValueError:
#                 st.warning(f"Error converting line to numbers: {line}")

#     if data:
#         visualize_data(data)

# def main():
#     st.title("Nadi and Health Metrics Processing")

#     mode = st.sidebar.selectbox("Select Mode", [
#         "Process Nadi Data (Single File)",
#         "Process Double Nadi Data",
#         "Get Health Metrics",
#         "Generate Comprehensive Nadi Report",
#         "Visualize Heart Rate Data"
#     ])

#     if mode == "Process Nadi Data (Single File)":
#         st.header("Process Nadi Data (Single File)")
#         file_source = st.text_input("Enter file path or URL")
#         hand = st.text_input("Enter hand parameter")
#         if st.button("Process"):
#             process_nadi(file_source, hand)

#     elif mode == "Process Double Nadi Data":
#         st.header("Process Double Nadi Data")
#         file_source1 = st.text_input("Enter first file path or URL")
#         file_source2 = st.text_input("Enter second file path or URL")
#         hand = st.text_input("Enter hand parameter")
#         if st.button("Process"):
#             process_nadi_double(file_source1, file_source2, hand)

#     elif mode == "Get Health Metrics":
#         st.header("Get Health Metrics")
#         file_source = st.text_input("Enter file path or URL")
#         if st.button("Get Metrics"):
#             get_health_metrics(file_source)

#     elif mode == "Generate Comprehensive Nadi Report":
#         st.header("Generate Comprehensive Nadi Report")
#         json_input_path = st.text_input("Enter JSON file path")
#         if st.button("Generate Report"):
#             generate_report(json_input_path)

#     elif mode == "Visualize Heart Rate Data":
#         st.header("Visualize Heart Rate Data")
#         filename = st.text_input("Enter the .txt file name or URL with pulse data")
#         if st.button("Visualize"):
#             if filename.startswith('http'):
#                 url_visualize_heart_rate_data(filename)
#             else:
#                 visualize_heart_rate_data(filename)


# if __name__ == '__main__':
#     main()

import json
import logging
import os
import time
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt

# Import your feature functions
from features.Nadi.functions_script import *
from features.Nadi.signal_process import *
from features.Nadi.nadi_processor_double import process_nadi_data_double
from features.Nadi.nadi_processor import process_nadi_data
from features.BP.predict_bp import predict_bp
from features.HeartRate.hr_calculation import estimate_heart_rate
from features.Temperature.TEMP_calculation import calculate_temperature
from features.SPO2.SPO2_calculation import calculate_spo2
from nadi_report.report_generation import create_comprehensive_pdf  # Import your PDF generation function

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app_terminal.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Allowed file extension for our text files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'

# Download file if a URL is provided
def download_file(url, dest_folder="tempFiles"):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    response = requests.get(url)
    if response.status_code != 200:
        logger.error("Failed to download file from URL")
        raise Exception("Failed to download file from URL")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_path = os.path.join(dest_folder, f'temp_file_{timestamp}.txt')
    with open(temp_path, 'wb') as f:
        f.write(response.content)
    return temp_path

def get_health_metrics(file_source):
    temp_download = False
    file_path = None
    try:
        if isinstance(file_source, str) and (file_source.startswith("http://") or file_source.startswith("https://")):
            file_path = download_file(file_source)
            temp_download = True
        else:
            # Handle file-like object from st.file_uploader
            file_path = os.path.join("tempFiles", f"uploaded_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(file_path, 'wb') as f:
                f.write(file_source.read())

        if not allowed_file(file_path):
            raise Exception("Invalid file type. Only '.txt' files are allowed.")

        data = {}

        try:
            systolic_bp, diastolic_bp = predict_bp(file_path)
            data['systolic_bp'] = systolic_bp
            data['diastolic_bp'] = diastolic_bp
        except Exception as e:
            logger.error(f"Error in predict_bp: {e}")
            raise Exception(f"Error in BP prediction: {e}")

        try:
            heart_rate = estimate_heart_rate(file_path)
            data['heart_rate'] = heart_rate
        except Exception as e:
            logger.error(f"Error in estimate_heart_rate: {e}")
            raise Exception(f"Error in heart rate calculation: {e}")

        try:
            temperature = calculate_temperature(file_path)
            data['temperature'] = temperature
        except Exception as e:
            logger.error(f"Error in calculate_temperature: {e}")
            raise Exception(f"Error in temperature calculation: {e}")

        try:
            spo2 = calculate_spo2(file_path)
            data['spo2'] = spo2
        except Exception as e:
            logger.error(f"Error in calculate_spo2: {e}")
            raise Exception(f"Error in SpO2 calculation: {e}")

        # # Add download button for the result
        # result_str = json.dumps(data, indent=4)
        # st.download_button(
        #     label="Download Health Metrics Result",
        #     data=result_str,
        #     file_name="health_metrics_result.json",
        #     mime="application/json"
        # )

        return data

    except Exception as e:
        logger.error(f"Error in get_health_metrics: {e}")
        st.error(f"Error: {e}")
        return None
    finally:
        if temp_download and file_path and os.path.exists(file_path):
            os.remove(file_path)


# Function to load data from a file-like object
def load_data_from_file(file):
    data = []
    try:
        for line in file:
            line = line.decode('utf-8').strip()  # Decode bytes to string
            if line:
                parts = line.split(',')
                if len(parts) != 3:
                    # st.warning(f"Skipping line (unexpected format): {line}")
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
    """Trim the data by taking only the latter half of the data points."""
    return data[len(data) // 2:] if len(data) > 1 else data

# Function to visualize the heart rate data
def visualize_data(data):
    if not data:
        st.error("No valid data to visualize.")
        return

    trimmed_data = trim_data(data)

    if len(trimmed_data[0]) < 3:
        st.error("Data must have at least 3 columns for visualization.")
        return

    x = list(range(1, len(trimmed_data) + 1))
    col1 = [row[0] for row in trimmed_data]
    col2 = [row[1] for row in trimmed_data]
    col3 = [row[2] for row in trimmed_data]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, col1, label='Data Series 1', linewidth=1.5)
    ax.plot(x, col2, label='Data Series 2', linewidth=1.5)
    ax.plot(x, col3, label='Data Series 3', linewidth=1.5)

    ax.set_title('Heart Rate Data Visualization')
    ax.set_xlabel('Measurement Index')
    ax.set_ylabel('Value')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Function to visualize data from a file
def visualize_heart_rate_data(file):
    data = load_data_from_file(file)
    if data:
        visualize_data(data)


st.title("N-PULSE DATA PROCESSING")
# Option to upload a file
st.sidebar.title("N-PLUSE")
uploaded_file = st.sidebar.file_uploader("Upload patient data text file", type="txt")
if uploaded_file:
    if uploaded_file is not None:
        if st.button("Process"):
            st.title("HEALTH METRICS")
            metrics = get_health_metrics(uploaded_file)
            if metrics:
                # Display the metrics in columns
                col3, col4, col5 = st.columns(3)
                with col3:
                    st.header("Heart Rate")
                    st.header(int(metrics.get('heart_rate', 0)))
                with col4:
                    st.header("Temperature")
                    st.header(int(metrics.get('temperature', 0)))
                with col5:
                    st.header("SpO2")
                    st.header(int(metrics.get('spo2', 0)))
                col1, col2= st.columns(2)
                with col1:
                    st.header("Diastolic BP")
                    st.header(int(metrics.get('diastolic_bp', 0)))
                with col2:
                    st.header("Systolic BP")
                    st.header(int(metrics.get('systolic_bp', 0)))

        # st.title("DATA VISUALIZATION")
        visualize_heart_rate_data(uploaded_file)
