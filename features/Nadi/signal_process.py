from features.Nadi.functions_script import *
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



class signal_process():
    def __init__(self,signal_raw,type,sample_freq):
        self.type=type
        self.sfreq=sample_freq
        self.signal_raw=signal_raw
        self.signal=self.filter()
        self.r_peaks,self.signal,self.FreqHeartRate=self.peaks()
        self.RMSSD,self.SDNN,self.TimeHeartRate,self.corrected_r_peaks=self.HRV()
        self.mean_SQI,self.SQI=self.corr()
        self.mean_BaseLength,self.mean_AUC,self.mean_Amplitude,self.mean_SystolicTime,self.mean_SystolicSlope=self.morphology()
        
    def filter(self):
        return (butter_bandpass_filter(self.signal_raw, lowcut=0.5, highcut=15,fs=self.sfreq, order=3))
    def peaks(self):
        #detect peaks
        r_peaks,signal,freq_heart_rate=peak_detect(self.signal,fs=self.sfreq)
        print('these are peaks')
        print(f'Detected peak length: {len(r_peaks)}')
        return r_peaks,signal,freq_heart_rate
    def HRV(self):
        rmssd,sdnn,time_heart_rate,corrected_rpeaks=hrv_from_rpeaks(self.r_peaks,sfreq=self.sfreq)
        print(f'Total number of heart rate measurements: {(time_heart_rate)}')
        return rmssd,sdnn,time_heart_rate,corrected_rpeaks
    def corr(self):
        cv,indv=corrCI(self.signal,self.r_peaks,plot=False)
        return cv,indv
    def morphology(self):
        f1k,f2k,f3k,f4k,f5k=morph(self.signal,self.r_peaks,self.SQI)
        return np.mean(f1k),np.mean(f2k),np.mean(f3k),np.mean(f4k),np.mean(f5k)
    