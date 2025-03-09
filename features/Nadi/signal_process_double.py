from features.Nadi.functions_script import *
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



class signal_process():
    def __init__(self,signal_raw1,signal_raw2,type,sample_freq):
        self.type=type
        self.sfreq=sample_freq
        #initiate two signals 
        self.signal_raw1=signal_raw1
        self.signal_raw2=signal_raw2
        #filter two signals 
        self.signal1=self.filter1()
        self.signal2=self.filter2()
        #get peaks for two signals 
        self.r_peaks1,self.signal1,self.FreqHeartRate1=self.peaks1()
        self.r_peaks2,self.signal2,self.FreqHeartRate2=self.peaks2()
        
        self.RMSSD,self.SDNN,self.TimeHeartRate,self.corrected_r_peaks=self.HRV()
        
        self.mean_SQI1,self.SQI1=self.corr1()
        self.mean_SQI2,self.SQI2=self.corr2()
        
        self.mean_BaseLength,self.mean_AUC,self.mean_Amplitude,self.mean_SystolicTime,self.mean_SystolicSlope=self.morphology()
        
    def filter1(self):
        return (butter_bandpass_filter(self.signal_raw1, lowcut=0.5, highcut=15,fs=self.sfreq, order=3))
    def filter2(self):
        return (butter_bandpass_filter(self.signal_raw2, lowcut=0.5, highcut=15,fs=self.sfreq, order=3))
    
    def peaks1(self):
        #detect peaks
        r_peaks,signal,freq_heart_rate=peak_detect(self.signal1,fs=self.sfreq)
        return r_peaks,signal,freq_heart_rate
    def peaks2(self):
        #detect peaks
        r_peaks,signal,freq_heart_rate=peak_detect(self.signal2,fs=self.sfreq)
        return r_peaks,signal,freq_heart_rate
    
    def HRV(self):
        rmssd,sdnn,time_heart_rate,corrected_rpeaks=hrv_from_rpeaks_double(self.r_peaks1,self.r_peaks2,sfreq=self.sfreq)
        return rmssd,sdnn,time_heart_rate,corrected_rpeaks
    
    def corr1(self):
        cv1,indv1=corrCI(self.signal1,self.r_peaks1,plot=False)
        return cv1,indv1
    
    def corr2(self):
        cv2,indv2=corrCI(self.signal2,self.r_peaks2,plot=False)
        return cv2,indv2
    
    def morphology(self):
        f1k,f2k,f3k,f4k,f5k=morph_double(self.signal1,self.signal2,self.r_peaks1,self.r_peaks2,
                                         self.SQI1,self.SQI2)
        return np.mean(f1k),np.mean(f2k),np.mean(f3k),np.mean(f4k),np.mean(f5k)
    
    
    