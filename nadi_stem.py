
import streamlit as st
import logging
import os
from nadi import signal_process
from features.Nadi.nadi_processor import process_nadi_data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from streamlit import title
from features.Nadi.signal_process import signal_process
import streamlit as st


def process_nadi_data(data_file, hand):
    df = pd.read_csv(data_file, skiprows=13, engine='python')
    sfreq = int(len(df) / 60)

    if hand == 'r':
        df_nadi = pd.DataFrame()
        df_nadi['Vatta'] = pd.to_numeric(df.iloc[:, 2], errors='coerce', downcast="float")
        df_nadi['Pitta'] = pd.to_numeric(df.iloc[:, 1], errors='coerce', downcast="float")
        df_nadi['Kapha'] = pd.to_numeric(df.iloc[:, 0], errors='coerce', downcast="float")
    elif hand == 'l':
        df_nadi = pd.DataFrame()
        df_nadi['Vatta'] = pd.to_numeric(df.iloc[:, 0], errors='coerce', downcast="float")
        df_nadi['Pitta'] = pd.to_numeric(df.iloc[:, 1], errors='coerce', downcast="float")
        df_nadi['Kapha'] = pd.to_numeric(df.iloc[:, 2], errors='coerce', downcast="float")

    V = -df_nadi['Vatta']
    P = -df_nadi['Pitta']
    K = -df_nadi['Kapha']

    Kapha = signal_process(signal_raw=K, type='Kapha', sample_freq=sfreq)
    Pitta = signal_process(signal_raw=P, type='Pitta', sample_freq=sfreq)
    Vatta = signal_process(signal_raw=V, type='Vatta', sample_freq=sfreq)

    a_HR = np.around(np.array([Kapha.TimeHeartRate, Pitta.TimeHeartRate, Vatta.TimeHeartRate]) / np.min(
        [Kapha.TimeHeartRate, Pitta.TimeHeartRate, Vatta.TimeHeartRate]), 2)
    a_HRV = np.around(np.array([Kapha.SDNN, Pitta.SDNN, Vatta.SDNN]) / np.min([Kapha.SDNN, Pitta.SDNN, Vatta.SDNN]), 0)
    a_auc = np.around(np.array([Kapha.mean_AUC, Pitta.mean_AUC, Vatta.mean_AUC]) / np.min(
        [Kapha.mean_AUC, Pitta.mean_AUC, Vatta.mean_AUC]), 0)
    a_amp = np.around(np.array([Kapha.mean_Amplitude, Pitta.mean_Amplitude, Vatta.mean_Amplitude]) / np.min(
        [Kapha.mean_Amplitude, Pitta.mean_Amplitude, Vatta.mean_Amplitude]), 0)
    a_st = np.around(np.array([Kapha.mean_SystolicTime, Pitta.mean_SystolicTime, Vatta.mean_SystolicTime]) / np.min(
        [Kapha.mean_SystolicTime, Pitta.mean_SystolicTime, Vatta.mean_SystolicTime]), 0)
    a_ss = np.around(np.array([Kapha.mean_SystolicSlope, Pitta.mean_SystolicSlope, Vatta.mean_SystolicSlope]) / np.min(
        [Kapha.mean_SystolicSlope, Pitta.mean_SystolicSlope, Vatta.mean_SystolicSlope]), 0)
    a_dc = np.around(np.array([df_nadi['Kapha'].mean().round(2), df_nadi['Pitta'].mean().round(2),
                               df_nadi['Vatta'].mean().round(2)]) / np.min(
        [df_nadi['Kapha'].mean().round(2), df_nadi['Pitta'].mean().round(2), df_nadi['Vatta'].mean().round(2)]), 0)

    len_sig = len(Vatta.signal)
    alp = len_sig - (sfreq * 3)
    bet = len_sig

    response = {
        "hand": hand,
        "processed_data": {
            "a_HR": a_HR.tolist(),
            "a_HRV": a_HRV.tolist(),
            "a_auc": a_auc.tolist(),
            "a_amp": a_amp.tolist(),
            "a_st": a_st.tolist(),
            "a_ss": a_ss.tolist(),
            "a_dc": a_dc.tolist(),
        },
        # "chart_data1": {
        #     "Vatta": Vatta.signal.tolist(),
        #     "Pitta": Pitta.signal.tolist(),
        #     "Kapha": Kapha.signal.tolist()
        # },

        # "single_beat_data": {
        #     "Vatta": Vatta.signal[alp:bet].tolist(),
        #     "Pitta": Pitta.signal[alp:bet].tolist(),
        #     "Kapha": Kapha.signal[alp:bet].tolist()
        # }
    }

    return response, V, P, K, sfreq


# Setup logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app_terminal.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Visualize heart rate data
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


# Load and process file data
def load_data_from_file(file):
    data = []
    try:
        file.seek(0)
        for line in file:
            line = line.decode("utf-8").strip()
            if line:
                parts = line.split(",")
                if len(parts) != 3:
                    continue
                try:
                    data.append(list(map(float, parts)))
                except ValueError:
                    logger.warning(f"Skipping invalid line: {line}")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        logger.error(f"Error reading file: {e}")
    return data


# Trim data function
def trim_data(data):
    return data[len(data) // 2:] if len(data) > 1 else data


# streamlit main app
def main():
    st.sidebar.title("N-PULSE")
    st.title("N-PULSE HEART DATA")
    uploaded_file = st.sidebar.file_uploader("📂Upload Data File", type=["txt"])
    hand = st.sidebar.selectbox("✋Select Hand", ["R", "L"]).lower()
    if st.sidebar.button("Process"):
        if not uploaded_file:
            st.warning("⚠️Please Upload Data File")
        else:
            response, V, P, K, sfreq = process_nadi_data(uploaded_file, hand)
            pulse_processor = signal_process(K, 'Kapha', sfreq)
            col1, col2 = st.columns(2)
            with col1:
                st.header("Detected Peaks")
                st.header(len(pulse_processor.r_peaks))
            with col2:
                st.header("Total No of Heart Rate Measurement")
                st.subheader(pulse_processor.TimeHeartRate)
            # st.header("📈Peaks Chart ")
            # st.line_chart(pulse_processor.signal)
            st.header("DATA VISUALIZATION")
            visualize_heart_rate_data(uploaded_file)


if __name__ == "__main__":
    main()


# import streamlit as st
# import logging
# import os
# from nadi import signal_process
# from features.Nadi.nadi_processor import process_nadi_data
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from streamlit import title
# from features.Nadi.signal_process import signal_process
# import streamlit as st
#
#
#
#
# def process_nadi_data(data_file, hand):
#     df = pd.read_csv(data_file, skiprows=13, engine='python')
#     sfreq = int(len(df) / 60)
#
#     if hand == 'r':
#         df_nadi = pd.DataFrame()
#         df_nadi['Vatta'] = pd.to_numeric(df.iloc[:, 2], errors='coerce', downcast="float")
#         df_nadi['Pitta'] = pd.to_numeric(df.iloc[:, 1], errors='coerce', downcast="float")
#         df_nadi['Kapha'] = pd.to_numeric(df.iloc[:, 0], errors='coerce', downcast="float")
#     elif hand == 'l':
#         df_nadi = pd.DataFrame()
#         df_nadi['Vatta'] = pd.to_numeric(df.iloc[:, 0], errors='coerce', downcast="float")
#         df_nadi['Pitta'] = pd.to_numeric(df.iloc[:, 1], errors='coerce', downcast="float")
#         df_nadi['Kapha'] = pd.to_numeric(df.iloc[:, 2], errors='coerce', downcast="float")
#
#     V = -df_nadi['Vatta']
#     P = -df_nadi['Pitta']
#     K = -df_nadi['Kapha']
#
#     Kapha = signal_process(signal_raw=K, type='Kapha', sample_freq=sfreq)
#     Pitta = signal_process(signal_raw=P, type='Pitta', sample_freq=sfreq)
#     Vatta = signal_process(signal_raw=V, type='Vatta', sample_freq=sfreq)
#
#     a_HR = np.around(np.array([Kapha.TimeHeartRate, Pitta.TimeHeartRate, Vatta.TimeHeartRate]) / np.min(
#         [Kapha.TimeHeartRate, Pitta.TimeHeartRate, Vatta.TimeHeartRate]), 2)
#     a_HRV = np.around(np.array([Kapha.SDNN, Pitta.SDNN, Vatta.SDNN]) / np.min([Kapha.SDNN, Pitta.SDNN, Vatta.SDNN]), 0)
#     a_auc = np.around(np.array([Kapha.mean_AUC, Pitta.mean_AUC, Vatta.mean_AUC]) / np.min(
#         [Kapha.mean_AUC, Pitta.mean_AUC, Vatta.mean_AUC]), 0)
#     a_amp = np.around(np.array([Kapha.mean_Amplitude, Pitta.mean_Amplitude, Vatta.mean_Amplitude]) / np.min(
#         [Kapha.mean_Amplitude, Pitta.mean_Amplitude, Vatta.mean_Amplitude]), 0)
#     a_st = np.around(np.array([Kapha.mean_SystolicTime, Pitta.mean_SystolicTime, Vatta.mean_SystolicTime]) / np.min(
#         [Kapha.mean_SystolicTime, Pitta.mean_SystolicTime, Vatta.mean_SystolicTime]), 0)
#     a_ss = np.around(np.array([Kapha.mean_SystolicSlope, Pitta.mean_SystolicSlope, Vatta.mean_SystolicSlope]) / np.min(
#         [Kapha.mean_SystolicSlope, Pitta.mean_SystolicSlope, Vatta.mean_SystolicSlope]), 0)
#     a_dc = np.around(np.array([df_nadi['Kapha'].mean().round(2), df_nadi['Pitta'].mean().round(2),
#                                df_nadi['Vatta'].mean().round(2)]) / np.min(
#         [df_nadi['Kapha'].mean().round(2), df_nadi['Pitta'].mean().round(2), df_nadi['Vatta'].mean().round(2)]), 0)
#
#     len_sig = len(Vatta.signal)
#     alp = len_sig - (sfreq * 3)
#     bet = len_sig
#
#     response = {
#         "hand": hand,
#         "processed_data": {
#             "a_HR": a_HR.tolist(),
#             "a_HRV": a_HRV.tolist(),
#             "a_auc": a_auc.tolist(),
#             "a_amp": a_amp.tolist(),
#             "a_st": a_st.tolist(),
#             "a_ss": a_ss.tolist(),
#             "a_dc": a_dc.tolist(),
#         },
#         # "chart_data1": {
#         #     "Vatta": Vatta.signal.tolist(),
#         #     "Pitta": Pitta.signal.tolist(),
#         #     "Kapha": Kapha.signal.tolist()
#         # },
#
#         # "single_beat_data": {
#         #     "Vatta": Vatta.signal[alp:bet].tolist(),
#         #     "Pitta": Pitta.signal[alp:bet].tolist(),
#         #     "Kapha": Kapha.signal[alp:bet].tolist()
#         # }
#     }
#
#     return response, V, P, K, sfreq
#
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
#
# # Visualize heart rate data
# def visualize_data(data):
#     if not data:
#         st.error("No valid data to visualize.")
#         return
#
#     trimmed_data = trim_data(data)
#     x = list(range(1, len(trimmed_data) + 1))
#     col1 = [row[0] for row in trimmed_data]
#     col2 = [row[1] for row in trimmed_data]
#     col3 = [row[2] for row in trimmed_data]
#
#     fig, ax = plt.subplots(figsize=(12, 6))
#     ax.plot(x, col1, label="Data Series 1", linewidth=1.5)
#     ax.plot(x, col2, label="Data Series 2", linewidth=1.5)
#     ax.plot(x, col3, label="Data Series 3", linewidth=1.5)
#
#     ax.set_title("Heart Rate Data Visualization")
#     ax.set_xlabel("Measurement Index")
#     ax.set_ylabel("Value")
#     ax.legend()
#     ax.grid(True)
#     plt.tight_layout()
#     st.pyplot(fig)
#
# # Function to visualize data from a file
# def visualize_heart_rate_data(file):
#     data = load_data_from_file(file)
#     if data:
#         visualize_data(data)
#
# # Load and process file data
# def load_data_from_file(file):
#     data = []
#     try:
#         file.seek(0)
#         for line in file:
#             line = line.decode("utf-8").strip()
#             if line:
#                 parts = line.split(",")
#                 if len(parts) != 3:
#                     continue
#                 try:
#                     data.append(list(map(float, parts)))
#                 except ValueError:
#                     logger.warning(f"Skipping invalid line: {line}")
#     except Exception as e:
#         st.error(f"Error reading file: {e}")
#         logger.error(f"Error reading file: {e}")
#     return data
#
# # Trim data function
# def trim_data(data):
#     return data[len(data) // 2 :] if len(data) > 1 else data
#
#
#
# # streamlit main app
# def main():
#     st.title("N-PULSE")
#     uploaded_file = st.file_uploader("📂Upload Data File",type=["txt"])
#     hand = st.selectbox("✋Select Hand",["R","L"]).lower()
#     if st.button("Process"):
#         if not uploaded_file:
#             st.warning("⚠️Please Upload Data File")
#         else:
#             response, V, P, K, sfreq = process_nadi_data(uploaded_file, hand)
#             pulse_processor = signal_process(K,'Kapha',sfreq)
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.header("Detected Peaks")
#                 st.header(len(pulse_processor.r_peaks))
#             with col2:
#                 st.header("Total No of Heart Rate Measurement")
#                 st.subheader(pulse_processor.TimeHeartRate)
#             st.header("📈Peaks Chart ")
#             st.line_chart(pulse_processor.signal)
#
#             st.header("DATA VISUALIZATION")
#             visualize_heart_rate_data(uploaded_file)
#
#
# if __name__ == "__main__":
#     main()