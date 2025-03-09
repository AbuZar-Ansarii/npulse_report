import pandas as pd
import numpy as np
from features.Nadi.signal_process_double import signal_process

def process_nadi_data_double(data_file1, data_file2, hand):
    df1 = pd.read_csv(data_file1, skiprows=13, engine='python')
    sfreq = int(len(df1) / 60)

    if hand == 'r':
        df_nadi1 = pd.DataFrame({
            'Vatta': pd.to_numeric(df1.iloc[:, 2], errors='coerce', downcast="float"),
            'Pitta': pd.to_numeric(df1.iloc[:, 1], errors='coerce', downcast="float"),
            'Kapha': pd.to_numeric(df1.iloc[:, 0], errors='coerce', downcast="float")
        })
    elif hand == 'l':
        df_nadi1 = pd.DataFrame({
            'Vatta': pd.to_numeric(df1.iloc[:, 0], errors='coerce', downcast="float"),
            'Pitta': pd.to_numeric(df1.iloc[:, 1], errors='coerce', downcast="float"),
            'Kapha': pd.to_numeric(df1.iloc[:, 2], errors='coerce', downcast="float")
        })

    V1, P1, K1 = -df_nadi1['Vatta'], -df_nadi1['Pitta'], -df_nadi1['Kapha']
    df2 = pd.read_csv(data_file2, skiprows=13, engine='python')

    if hand == 'r':
        df_nadi2 = pd.DataFrame({
            'Vatta': pd.to_numeric(df2.iloc[:, 2], errors='coerce', downcast="float"),
            'Pitta': pd.to_numeric(df2.iloc[:, 1], errors='coerce', downcast="float"),
            'Kapha': pd.to_numeric(df2.iloc[:, 0], errors='coerce', downcast="float")
        })
    elif hand == 'l':
        df_nadi2 = pd.DataFrame({
            'Vatta': pd.to_numeric(df2.iloc[:, 0], errors='coerce', downcast="float"),
            'Pitta': pd.to_numeric(df2.iloc[:, 1], errors='coerce', downcast="float"),
            'Kapha': pd.to_numeric(df2.iloc[:, 2], errors='coerce', downcast="float")
        })

    V2, P2, K2 = -df_nadi2['Vatta'], -df_nadi2['Pitta'], -df_nadi2['Kapha']

    Kapha = signal_process(signal_raw1=K1, signal_raw2=K2, type='Kapha', sample_freq=sfreq)
    Pitta = signal_process(signal_raw1=P1, signal_raw2=P2, type='Pitta', sample_freq=sfreq)
    Vatta = signal_process(signal_raw1=V1, signal_raw2=V2, type='Vatta', sample_freq=sfreq)

    # Use signal1 for processing or select appropriate signal
    len_sig = len(Vatta.signal1)
    alp = len_sig - (sfreq * 3)
    bet = len_sig

    a_HR = np.around(np.array([Kapha.TimeHeartRate, Pitta.TimeHeartRate, Vatta.TimeHeartRate]) / 
                     np.min([Kapha.TimeHeartRate, Pitta.TimeHeartRate, Vatta.TimeHeartRate]), 2)
    a_HRV = np.around(np.array([Kapha.SDNN, Pitta.SDNN, Vatta.SDNN]) / 
                      np.min([Kapha.SDNN, Pitta.SDNN, Vatta.SDNN]), 0)
    a_auc = np.around(np.array([Kapha.mean_AUC, Pitta.mean_AUC, Vatta.mean_AUC]) / 
                      np.min([Kapha.mean_AUC, Pitta.mean_AUC, Vatta.mean_AUC]), 0)
    a_amp = np.around(np.array([Kapha.mean_Amplitude, Pitta.mean_Amplitude, Vatta.mean_Amplitude]) / 
                      np.min([Kapha.mean_Amplitude, Pitta.mean_Amplitude, Vatta.mean_Amplitude]), 0)
    a_st = np.around(np.array([Kapha.mean_SystolicTime, Pitta.mean_SystolicTime, Vatta.mean_SystolicTime]) / 
                     np.min([Kapha.mean_SystolicTime, Pitta.mean_SystolicTime, Vatta.mean_SystolicTime]), 0)
    a_ss = np.around(np.array([Kapha.mean_SystolicSlope, Pitta.mean_SystolicSlope, Vatta.mean_SystolicSlope]) / 
                     np.min([Kapha.mean_SystolicSlope, Pitta.mean_SystolicSlope, Vatta.mean_SystolicSlope]), 0)

    k_mean = (df_nadi1['Kapha'].mean().round(2) + df_nadi2['Kapha'].mean().round(2)) / 2
    p_mean = (df_nadi1['Pitta'].mean().round(2) + df_nadi2['Pitta'].mean().round(2)) / 2
    v_mean = (df_nadi1['Vatta'].mean().round(2) + df_nadi2['Vatta'].mean().round(2)) / 2
    a_dc = np.around(np.array([k_mean, p_mean, v_mean]) / np.min([k_mean, p_mean, v_mean]), 0)

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
        "chart_data1": {
            "Vatta": Vatta.signal1.tolist(),  # Adjusted to signal1
            "Pitta": Pitta.signal1.tolist(),
            "Kapha": Kapha.signal1.tolist()
        },
        "single_beat_data": {
            "Vatta": Vatta.signal1[alp:bet].tolist(),
            "Pitta": Pitta.signal1[alp:bet].tolist(),
            "Kapha": Kapha.signal1[alp:bet].tolist()
        }
    }

    return response
