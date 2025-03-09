import pandas as pd
import numpy as np
from features.Nadi.signal_process import signal_process


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


    a_HR = np.around(np.array([Kapha.TimeHeartRate, Pitta.TimeHeartRate, Vatta.TimeHeartRate]) / np.min([Kapha.TimeHeartRate, Pitta.TimeHeartRate, Vatta.TimeHeartRate]), 2)
    a_HRV = np.around(np.array([Kapha.SDNN, Pitta.SDNN, Vatta.SDNN]) / np.min([Kapha.SDNN, Pitta.SDNN, Vatta.SDNN]), 0)
    a_auc = np.around(np.array([Kapha.mean_AUC, Pitta.mean_AUC, Vatta.mean_AUC]) / np.min([Kapha.mean_AUC, Pitta.mean_AUC, Vatta.mean_AUC]), 0)
    a_amp = np.around(np.array([Kapha.mean_Amplitude, Pitta.mean_Amplitude, Vatta.mean_Amplitude]) / np.min([Kapha.mean_Amplitude, Pitta.mean_Amplitude, Vatta.mean_Amplitude]), 0)
    a_st = np.around(np.array([Kapha.mean_SystolicTime, Pitta.mean_SystolicTime, Vatta.mean_SystolicTime]) / np.min([Kapha.mean_SystolicTime, Pitta.mean_SystolicTime, Vatta.mean_SystolicTime]), 0)
    a_ss = np.around(np.array([Kapha.mean_SystolicSlope, Pitta.mean_SystolicSlope, Vatta.mean_SystolicSlope]) / np.min([Kapha.mean_SystolicSlope, Pitta.mean_SystolicSlope, Vatta.mean_SystolicSlope]), 0)
    a_dc = np.around(np.array([df_nadi['Kapha'].mean().round(2), df_nadi['Pitta'].mean().round(2), df_nadi['Vatta'].mean().round(2)]) / np.min([df_nadi['Kapha'].mean().round(2), df_nadi['Pitta'].mean().round(2), df_nadi['Vatta'].mean().round(2)]), 0)

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

    return response