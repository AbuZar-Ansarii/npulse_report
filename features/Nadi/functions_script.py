#IMPORT LIBRARIES 
# !pip install hrv-analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA
import scipy
from scipy import signal
import seaborn
from sklearn.decomposition import PCA
from sklearn import preprocessing
import seaborn as sns 
from sklearn.preprocessing import MinMaxScaler
from scipy.signal import find_peaks,hilbert
from scipy.stats import gaussian_kde
from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values,get_time_domain_features
from scipy.signal import butter, lfilter
np.set_printoptions(precision=2)

from botocore.exceptions import ClientError
import boto3
import requests 
import streamlit as st

import io

# def upload_to_aws(data_file, bucket, s3_folder):
#     if data_file is not None:
#         s3 = boto3.client(
#             service_name="s3",
#             region_name=st.secrets["AWS_DEFAULT_REGION"],
#             aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
#             aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
#         )

#         name =  s3_folder + data_file.name 
#         s3.upload_fileobj(data_file, bucket, name)
#         st.write('Done uploading')

# def upload_processed_df_to_aws(df,bucket,s3_folder,data_file_name):
#     s3 = boto3.client(
#     service_name="s3",
#     region_name=st.secrets["AWS_DEFAULT_REGION"],
#     aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
#     aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
#                     )
#     name =  s3_folder + data_file_name[:-3]+'.csv'
#     with io.StringIO() as csv_buffer:
#         df.to_csv(csv_buffer, index=False)

#         response = s3.put_object(
#           Bucket=bucket, Key=name, Body=csv_buffer.getvalue()
#             ) 

# def upload_plot_to_aws(plot,bucket,s3_folder,data_file_name):
#     s3 = boto3.client(
#     service_name="s3",
#     region_name=st.secrets["AWS_DEFAULT_REGION"],
#     aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
#     aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
#                     )
#     name =  s3_folder + data_file_name[:-3]+'png'
#     with io.BytesIO() as img_data:
#         plot.savefig(img_data, format='png')
#         img_data.seek(0)

#         response = s3.put_object(
#           Bucket=bucket, Key=name, Body=img_data,ContentType='image/png'
#             ) 


##############################################################################################
def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
##############################################################################################
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
##############################################################################################
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    
    return y
##############################################################################################
#frequency spectrum 
def plot_welch(sg,fs,length,color,overlap)  :  
#     f, Pxx_den = signal.welch(sg, fs,nperseg=length,noverlap=overlap)
    sfreq=fs
    sg=sg[int(sfreq*7):-int(sfreq*2)]
    Pxx_den,f= mne.time_frequency.psd_array_welch(sg,fmin=0.4, fmax=2.5, sfreq=sfreq, n_fft=(sfreq)*5,n_per_seg=(sfreq)*5,n_overlap=(sfreq),verbose=False)
#     Pxx_den,f=mne.time_frequency.psd_array_multitaper(sg[int(sfreq)*2:], sfreq, fmin=0.4, fmax=2.5, bandwidth=0.25, adaptive=False, low_bias=True, normalization='length', n_jobs=1, verbose=None)
#     ll=np.where(f<=0.5)[0][-1]
#     ul=np.where(f>=2.5)[0][0]
    max_peak=np.argmax(Pxx_den[:])
#     f=f[ll:ul]
#     Pxx_den=Pxx_den[ll:ul]

# #     plt.figure()
#     plt.plot(f,Pxx_den,color=color)
# #     plt.semilogy(f, Pxx_den.T,color=color)
#     plt.plot(f[max_peak],Pxx_den[max_peak],'ro')
    
# #     plt.xlim([0.5, 20])
#     plt.xlabel('frequency [Hz]')
#     plt.ylabel('PSD [V**2/Hz]')
#     plt.tight_layout()
    
#     plt.show()
#     return f[max_peak]
##############################################################################################
def envolope(sig):
    analytic_signal = hilbert(sig)
    amp = np.abs(analytic_signal)
    ana= hilbert(amp)
    amplitude_envelope = np.abs(ana)
    plt.figure(figsize=(20,10))
    plt.plot(sig)
    plt.plot(amplitude_envelope,'r')
    plt.show()
    
    
#     return amplitude_envelope
##############################################################################################
def peak_detect(sig,fs):
#     [int(sfreq*7):-int(sfreq*2)]
    filt=pd.DataFrame()
    #filter signal between 0.4 Hz to 5 Hz Butterworth IIR filter of order 3
    filt['Signal']=butter_bandpass_filter(sig, lowcut=0.4, highcut=5,fs=400, order=3)
    
    ##Signal smoothening using rolling mean or moving averge of 0.25 seconds or 100 samples 
    rol=filt.rolling(100).mean().dropna().to_numpy()
    
    ##diffrentiation of the smoothened signal 
    dif=np.diff(rol.T)
    sfreq=fs
    
    ##Removing the begining of the diffrentiated signal because -
    ## - it has very high amplitude due to edge effect of the filter. 
    ##- Therefore we remove the begining part of the signal 
    #sg=filt.iloc[int(sfreq*7):].to_numpy().reshape(-1)
    sg=(dif.T).reshape(-1)
    sg=sg[int(sfreq*7):]
    
    #Find welch PSD of the diffrentated signal between 0.4 HZ to 2.5 Hz with 5 seconds moving PSD and 1 sec overlap.
#     Pxx_den,f= mne.time_frequency.psd_array_welch(sg,fmin=0.4, fmax=2.5, sfreq=sfreq, n_fft=(sfreq)*5,n_per_seg=(sfreq)*5,n_overlap=(sfreq),verbose=False)
    fnew, Pxx_dennew = signal.welch(sg, fs=sfreq, nperseg=(sfreq)*5, noverlap=sfreq, nfft=(sfreq)*5)
    fmin=0.4
    fmax=2.5
    fmin_index=np.argwhere(fnew<=fmin)
    fmin_index=fmin_index[-1]
    fmax_index=np.argwhere(fnew>=fmax)
    fmax_index=fmax_index[0]
    fnew=fnew[fmin_index[0]:fmax_index[0]]
    Pxx_dennew=Pxx_dennew[fmin_index[0]:fmax_index[0]]
    
    #find the freq with the maximum amplitude
#     max_peak=np.argmax(Pxx_den[:])
    max_peaknew=np.argmax(Pxx_dennew[:])
    
    
    #calcuate the prossible heart rate 
    fd_heart_rate=(1/fnew[max_peaknew])
    
    #calculate the mimimum distance between peaks for peak detection in the next step. 
    #This is 75% of the possible heart rate to account for heart rate variabliity.
    min_distance_between_peaks_samples=fd_heart_rate*0.75*sfreq
    
    
    ##Removing the begining of the diffrentiated signal because -
    ## - it has very high amplitude due to edge effect of the filter. 
    ##- Therefore we remove the begining part 5 seconds  of the signal 
    new_sig=(filt.to_numpy().T).reshape(-1)[(sfreq*5):]
    sig=sig[(sfreq*5):]
    #find peaks using the signal.find_peaks fucntion from scipy
    r_peaks,_= find_peaks(new_sig, distance=min_distance_between_peaks_samples)
    

    #plot PSD between 0.4Hz and 2.5 Hz
#     plt.figure()
#     plt.plot(fnew,Pxx_dennew,'b')
#     plt.plot(fnew[max_peaknew],Pxx_dennew[max_peaknew],'ro')
#     plt.xlabel('frequency [Hz]')
#     plt.ylabel('PSD [V**2/Hz]')
#     plt.tight_layout()
    
    #plot peaks detected
#     plt.figure(figsize=(20,10))
#     plt.plot(new_sig)
#     plt.plot(r_peaks,new_sig[r_peaks],'ro')
#     plt.show()
    
    #find the envolope of the signal
#     envolope(new_sig)
    
    heart_rate=fnew[max_peaknew]*60
    return r_peaks,sig,heart_rate

##############################################################################################
def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)
##############################################################################################
def moving_std(x,n):
    s=pd.Series(x)
    return (s.rolling(n).std())
##############################################################################################    
def corrCI(cleaned,r_peaks,plot):
    """Find the Average correlation between individual heart beats in a signal window 
    Parameters
    ----------
    CLEANED: numpy.array 
        signal array
    r_peaks : numpy.array
        corresponding r_peaks
        
    Returns
    -------
    float
       Average Coorelation coefficient for the signal window  
    """
    if plot:
        plt.figure()
        plt.xlabel('Samples')
        plt.ylabel('Amplitude')
        plt.title('Individual heat beats')   
        
    # VARIABLE TO STORE CORELATION BETWEEN INIDIVIDUAL HEART BEATS     
    corr=[]
    ind=[]
    # FOR EACH HEART BEAT FIND THE COORELATION WITH VERY OTHER HEARTBEAT 
    for i in range(len(r_peaks)-2):
        
    # GET INDIVIDUAL HEARTBEAT USING INDICES FROM R_PEAKS 
        current_peak=r_peaks[i]
        skiped_peak=r_peaks[i+1]
        following_peak=r_peaks[i+2]
        current_wind=cleaned[current_peak:following_peak]
        ind_corr=[]
    # GET ALL OTHER INDIVIDUAL HEARTBEAT USING INDICES FROM R_PEAKS AND RESAMPLE TO SAME LENGTH BEFORE USING THE COORELATION      FUNCTION 
        for j in range(len(r_peaks)-2):
         if j > i+2:
            next_peak=r_peaks[j]
            next_following_peak=r_peaks[j+2]
            next_wind=cleaned[next_peak:next_following_peak]
            next_wind=signal.resample(next_wind, len(current_wind))
            
            
            # FIND COORELATION BETWEEN TWO INDIVIDUAL HEART BEATS     
            coef=np.corrcoef(current_wind,next_wind)
            
            # SAVE THE COORELATION COEFFICIENT 
            
            corr=np.append(corr,coef)
            
            ind_corr=np.append(ind_corr,coef)
        ind=    np.append(ind,np.mean(ind_corr))
       
        if plot and ind[-1]>0.80:
                
                plt.plot(current_wind)
    #CALCULATE THE MEAN OF ALL COORELATION COEFFICIENTS IN THE SAME WINDOW
#     plt.figure(figsize=(20,10))
#     plt.plot(ind,'r')

    
    corrCi=np.mean(corr)       
    return corrCi,ind
##############################################################################################
def hrv_from_rpeaks(rr,sfreq):          
    """Computes the HRV features for the given array of rr peak intervals. Parameter selected to be returned are 
    SDNN, RMSSD, and mean heart rate. 
    This function uses an external library - https://github.com/Aura-healthcare/hrv-analysis
    More information :https://www.ncbi.nlm.nih.gov/labs/pmc/articles/PMC5624990/
    Parameters
    ----------
    rr : numpy array of rr intervals in milliseconds extracted from r_peaks detected.eg [700,850,100,960] 
    sfreq : int or None
        Sampling rate of the data. If None, it will be inferred from the data, but it requires a Timestamp column.

    Returns
    -------
    numpy.array with RMSSD,SDNN,mean heart rate and corrected rr_intervals.
    """
    #convert rr peaks to Inter beat interval or RR-interval
    rr=(np.diff(rr)*1000)/sfreq
    #lower limit of rr intervals is 600 msec and upper limit is 2500msec.
    # This remove outliers from signal that are not in this range 
    rr_intervals_without_outliers = remove_outliers(rr_intervals=rr,low_rri=300, high_rri=3000, verbose=False)
    # This replace outliers nan values with linear interpolation
    r_peaks = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,interpolation_method="linear")
    # This remove ectopic beats from signal - beats that are in the optimum range but are away from the mean rr interval
    r_peaks=np.array(r_peaks).astype(int)
    r_peaks = r_peaks[np.logical_not(np.isnan(r_peaks))]
    nn_intervals_list = remove_ectopic_beats(rr_intervals=r_peaks, method="malik", verbose=False)
    # This replace ectopic beats nan values with linear interpolation
    r_peaks = interpolate_nan_values(rr_intervals=nn_intervals_list)
    #Get HRV features of this window using the get_time_domain_features() function from hrv-analysis package 
    tf = get_time_domain_features(r_peaks)
    hrv_sdnn= tf['sdnn']      #in msec 
    hrv_rmssd=tf['rmssd']     #in msec
    mean_HR=tf['mean_hr']     #in Beats per minute 
#     print(hrv_sdnn)
#     print(hrv_rmssd)
#     print(mean_HR)
    
    # #double check if the HRV and mean Heart rate are in normal ranges based on -  https://www.sciencedirect.com/science/article/pii/S0735109797005548
    # if (((hrv_sdnn>300) or  (hrv_sdnn <0)) or ((hrv_rmssd>150) or  (hrv_rmssd <0))) :
    #     hrv_sdnn= -1   #in msec 
    #     hrv_rmssd=-1    #in msec
         #in Beats per minute
    return hrv_rmssd,hrv_sdnn, mean_HR, r_peaks


def hrv_from_rpeaks_double(rr1,rr2,sfreq):          
    """Computes the HRV features for the given array of rr peak intervals. Parameter selected to be returned are 
    SDNN, RMSSD, and mean heart rate. 
    This function uses an external library - https://github.com/Aura-healthcare/hrv-analysis
    More information :https://www.ncbi.nlm.nih.gov/labs/pmc/articles/PMC5624990/
    Parameters
    ----------
    rr : numpy array of rr intervals in milliseconds extracted from r_peaks detected.eg [700,850,100,960] 
    sfreq : int or None
        Sampling rate of the data. If None, it will be inferred from the data, but it requires a Timestamp column.

    Returns
    -------
    numpy.array with RMSSD,SDNN,mean heart rate and corrected rr_intervals.
    """
    #convert rr peaks to Inter beat interval or RR-interval
    rr1=(np.diff(rr1)*1000)/sfreq
    rr2=(np.diff(rr2)*1000)/sfreq
    
    rr=np.concatenate((rr1,rr2))
    #lower limit of rr intervals is 600 msec and upper limit is 2500msec.
    # This remove outliers from signal that are not in this range 
    rr_intervals_without_outliers = remove_outliers(rr_intervals=rr,low_rri=300, high_rri=3000, verbose=False)
    # This replace outliers nan values with linear interpolation
    r_peaks = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,interpolation_method="linear")
    # This remove ectopic beats from signal - beats that are in the optimum range but are away from the mean rr interval
    r_peaks=np.array(r_peaks).astype(int)
    r_peaks = r_peaks[np.logical_not(np.isnan(r_peaks))]
    nn_intervals_list = remove_ectopic_beats(rr_intervals=r_peaks, method="malik", verbose=False)
    # This replace ectopic beats nan values with linear interpolation
    r_peaks = interpolate_nan_values(rr_intervals=nn_intervals_list)
    #Get HRV features of this window using the get_time_domain_features() function from hrv-analysis package 
    tf = get_time_domain_features(r_peaks)
    hrv_sdnn= tf['sdnn']      #in msec 
    hrv_rmssd=tf['rmssd']     #in msec
    mean_HR=tf['mean_hr']     #in Beats per minute 
#     print(hrv_sdnn)
#     print(hrv_rmssd)
#     print(mean_HR)
    
    # #double check if the HRV and mean Heart rate are in normal ranges based on -  https://www.sciencedirect.com/science/article/pii/S0735109797005548
    # if (((hrv_sdnn>300) or  (hrv_sdnn <0)) or ((hrv_rmssd>150) or  (hrv_rmssd <0))) :
    #     hrv_sdnn= -1   #in msec 
    #     hrv_rmssd=-1    #in msec
         #in Beats per minute
    return hrv_rmssd,hrv_sdnn, mean_HR, r_peaks



##########
##morphological features 
##############################################################################################
def systole_amplitude(pulse):
    """Find the amplitude of a single pulse or the systolic peak  
    Parameters
    ----------
    pulse: numpy.array 
        signal array
    Returns
    -------
    float
       peak amplitude value of the single pulse  
    """
    return np.max(pulse)
##############################################################################################
def systolic_time(pulse):
    """Find the time taken to reach maximum point or the systolic peak  of a single pulse 
    Parameters
    ----------
    pulse: numpy.array 
        signal array
    Returns
    -------
    float
       time to reach peak amplitude value of the single pulse  
    """
    return np.argmax(pulse)
##############################################################################################
def slope_of_systole(pulse):
    """Find the time taken to reach maximum point or the systolic peak  of a single pulse 
    Parameters
    ----------
    pulse: numpy.array 
        signal array
    Returns
    -------
    float
       time to reach peak amplitude value of the single pulse  
    """
    base=np.argmax(pulse)
    height=np.max(pulse)
    # Assuming this is the calculation on line 366
    # Replace this line
    # fraction = height / base

    # With this check
    if base == 0:
        # logging.warning("Base is zero, returning NaN for fraction.")
        fraction = np.nan  # or set a default value
    else:
        fraction = height / base

    # Similarly for any other calculations that involve division or could potentially result in NaN values.

    slope= np.arctan(fraction)
    
    return slope

    
##############################################################################################    
def morph(cleaned,r_peaks,ind):
    """Find the Average correlation between individual heart beats in a signal window 
    Parameters
    ----------
    CLEANED: numpy.array 
        signal array
    r_peaks : numpy.array
        corresponding r_peaks
    ind:Siganl quailty index    
        array
    Returns
    -------
    float
       Average Coorelation coefficient for the signal window  
    """
    
        # plt.figure(figsize=(10,7))
        # plt.xlabel('Samples')
        # plt.ylabel('Amplitude')
        # plt.title('Individual heat beats')   

    # VARIABLE TO STORE features from INIDIVIDUAL HEART BEATS     
    #f1
    base_distance_cumal=[]
    #f2
    area_under_curve_cumal=[]
    #f3
    systole_amp_cumal=[]
    #f4
    syst_time_cumal=[]
    #f5
    slope_of_syst_cumal=[]
    
    
    
    # FOR EACH HEART BEAT FIND THE COORELATION WITH VERY OTHER HEARTBEAT 
    for i in range(len(r_peaks)-2):
    # GET INDIVIDUAL HEARTBEAT USING INDICES FROM R_PEAKS 
        current_peak=r_peaks[i]
        skiped_peak=r_peaks[i+1]
        following_peak=r_peaks[i+2]
        # if ind[i]>0.70:
        if True:    
            
            #extract individual pulse# 
            base_start=np.argmin(cleaned[current_peak:skiped_peak])
            reminder=len(cleaned[current_peak:skiped_peak])-base_start
            base_end=np.argmin(cleaned[skiped_peak:following_peak])+reminder
            ref1=current_peak+base_start
            ref2=ref1+base_end
            current_wind=cleaned[ref1:ref2]
            ###############################
            
            #remove  DC offset# 
            offset=np.mean([current_wind[0],current_wind[-1]])
            if offset<0:
                current_wind=np.abs(offset)+current_wind
            elif offset>0:
                current_wind=current_wind-offset 
            ###############################
            
            #plot window#     
            # plt.plot(current_wind)   
            ###############################
            
            #the pulses are ready for features#    
            #now lets extract morphological featurs     
                
            #feature list 
            ################
            ##feature 1 -- Width of the pulse on xaxis or the number of samples between the start of end of pulse
            base_dist=len(current_wind)
            base_distance_cumal=np.append(base_distance_cumal,base_dist)
            ################
            
            ################
            #feature 2 -- Area under curve for all ac pulses
            auc=np.trapz(current_wind)
            area_under_curve_cumal=np.append(area_under_curve_cumal,auc)
            ################
            
            ################
            #feature 3 -- Systolic amplitude 
            systole_amp=systole_amplitude(current_wind)
            systole_amp_cumal=np.append(systole_amp_cumal,systole_amp)
            ################
            
            ################
            #feature 4 -- Systolic time
            systole_time=systolic_time(current_wind)
            syst_time_cumal=np.append(syst_time_cumal,systole_time)
            ################
            
            ################
            #feature 5 -- Systolic slope
            systole_slope=slope_of_systole(current_wind)
            slope_of_syst_cumal=np.append(slope_of_syst_cumal,systole_slope)
            ################
            
            
            
    return  base_distance_cumal,area_under_curve_cumal,systole_amp_cumal,syst_time_cumal,slope_of_syst_cumal
    
    
    
    
    #############


##############################################################################################    
def morph_double(cleaned1,cleaned2,r_peaks1,r_peaks2,ind1,ind2):
    """Find the Average correlation between individual heart beats in a signal window 
    Parameters
    ----------
    CLEANED: numpy.array 
        signal array
    r_peaks : numpy.array
        corresponding r_peaks
    ind:Siganl quailty index    
        array
    Returns
    -------
    float
       Average Coorelation coefficient for the signal window  
    """
    
        # plt.figure(figsize=(10,7))
        # plt.xlabel('Samples')
        # plt.ylabel('Amplitude')
        # plt.title('Individual heat beats')   

    # VARIABLE TO STORE features from INIDIVIDUAL HEART BEATS     
    #f1
    base_distance_cumal=[]
    #f2
    area_under_curve_cumal=[]
    #f3
    systole_amp_cumal=[]
    #f4
    syst_time_cumal=[]
    #f5
    slope_of_syst_cumal=[]
    
    
    
    # FOR EACH HEART BEAT FIND THE COORELATION WITH VERY OTHER HEARTBEAT 
    for i in range(len(r_peaks1)-2):
    # GET INDIVIDUAL HEARTBEAT USING INDICES FROM R_PEAKS 
        current_peak=r_peaks1[i]
        skiped_peak=r_peaks1[i+1]
        following_peak=r_peaks1[i+2]
        # if ind[i]>0.70:
        if True:    
            
            #extract individual pulse# 
            base_start=np.argmin(cleaned1[current_peak:skiped_peak])
            reminder=len(cleaned1[current_peak:skiped_peak])-base_start
            base_end=np.argmin(cleaned1[skiped_peak:following_peak])+reminder
            ref1=current_peak+base_start
            ref2=ref1+base_end
            current_wind=cleaned1[ref1:ref2]
            ###############################
            
            #remove  DC offset# 
            offset=np.mean([current_wind[0],current_wind[-1]])
            if offset<0:
                current_wind=np.abs(offset)+current_wind
            elif offset>0:
                current_wind=current_wind-offset 
            ###############################
            
            #plot window#     
            # plt.plot(current_wind)   
            ###############################
            
            #the pulses are ready for features#    
            #now lets extract morphological featurs     
                
            #feature list 
            ################
            ##feature 1 -- Width of the pulse on xaxis or the number of samples between the start of end of pulse
            base_dist=len(current_wind)
            base_distance_cumal=np.append(base_distance_cumal,base_dist)
            ################
            
            ################
            #feature 2 -- Area under curve for all ac pulses
            auc=np.trapz(current_wind)
            area_under_curve_cumal=np.append(area_under_curve_cumal,auc)
            ################
            
            ################
            #feature 3 -- Systolic amplitude 
            systole_amp=systole_amplitude(current_wind)
            systole_amp_cumal=np.append(systole_amp_cumal,systole_amp)
            ################
            
            ################
            #feature 4 -- Systolic time
            systole_time=systolic_time(current_wind)
            syst_time_cumal=np.append(syst_time_cumal,systole_time)
            ################
            
            ################
            #feature 5 -- Systolic slope
            systole_slope=slope_of_systole(current_wind)
            slope_of_syst_cumal=np.append(slope_of_syst_cumal,systole_slope)
            ################
            
    
    # FOR EACH HEART BEAT FIND THE COORELATION WITH VERY OTHER HEARTBEAT 
    for i in range(len(r_peaks2)-2):
    # GET INDIVIDUAL HEARTBEAT USING INDICES FROM R_PEAKS 
        current_peak=r_peaks2[i]
        skiped_peak=r_peaks2[i+1]
        following_peak=r_peaks2[i+2]
        # if ind[i]>0.70:
        if True:    
            
            #extract individual pulse# 
            base_start=np.argmin(cleaned2[current_peak:skiped_peak])
            reminder=len(cleaned2[current_peak:skiped_peak])-base_start
            base_end=np.argmin(cleaned2[skiped_peak:following_peak])+reminder
            ref1=current_peak+base_start
            ref2=ref1+base_end
            current_wind=cleaned2[ref1:ref2]
            ###############################
            
            #remove  DC offset# 
            offset=np.mean([current_wind[0],current_wind[-1]])
            if offset<0:
                current_wind=np.abs(offset)+current_wind
            elif offset>0:
                current_wind=current_wind-offset 
            ###############################
            
            #plot window#     
            # plt.plot(current_wind)   
            ###############################
            
            #the pulses are ready for features#    
            #now lets extract morphological featurs     
                
            #feature list 
            ################
            ##feature 1 -- Width of the pulse on xaxis or the number of samples between the start of end of pulse
            base_dist=len(current_wind)
            base_distance_cumal=np.append(base_distance_cumal,base_dist)
            ################
            
            ################
            #feature 2 -- Area under curve for all ac pulses
            auc=np.trapz(current_wind)
            area_under_curve_cumal=np.append(area_under_curve_cumal,auc)
            ################
            
            ################
            #feature 3 -- Systolic amplitude 
            systole_amp=systole_amplitude(current_wind)
            systole_amp_cumal=np.append(systole_amp_cumal,systole_amp)
            ################
            
            ################
            #feature 4 -- Systolic time
            systole_time=systolic_time(current_wind)
            syst_time_cumal=np.append(syst_time_cumal,systole_time)
            ################
            
            ################
            #feature 5 -- Systolic slope
            systole_slope=slope_of_systole(current_wind)
            slope_of_syst_cumal=np.append(slope_of_syst_cumal,systole_slope)
            ################
                    
            
    return  base_distance_cumal,area_under_curve_cumal,systole_amp_cumal,syst_time_cumal,slope_of_syst_cumal
    
    
    
    
    #############
    
#ica for breath pattern
def ICAA(df):
    """Perfrom Independed component analysis using sklearn FastICA 
    Parameters
    ----------
    data : numpy.array
        eeg data filtered 
    Returns
    -------
    numpy.ndarray
        Array of independent components 
    """
    ica = FastICA(n_components=df.shape[1],random_state=5,whiten=True)
    S_ = ica.fit_transform(df)
    df.iloc[7000:].plot(subplots=True,figsize=(50,10))
#     plt.figure(figsize=(20,10))
    fig, axs = plt.subplots(3, 1,figsize=(50,10))
    axs[0].plot(S_[7000:,0])
    axs[1].plot(S_[7000:,1])  
    axs[2].plot(S_[7000:,2])    
    return S_

def PCAA(df):
    """Perfrom Independed component analysis using sklearn FastICA 
    Parameters
    ----------
    data : numpy.array
    eeg data filtered 
    Returns
    -------
    numpy.ndarray
    Array of independent components 
    """
    ica = PCA(n_components=df.shape[1],random_state=5)
    S_ = ica.fit_transform(df)
    df.iloc[7000:].plot(subplots=True,figsize=(50,10))
#     plt.figure(figsize=(20,10))
    fig, axs = plt.subplots(3, 1,figsize=(50,10))
    axs[0].plot(S_[7000:,0])
    axs[1].plot(S_[7000:,1])  
    axs[2].plot(S_[7000:,2])    
    return S_
########################################################################################
def dff_make(pulse,name,day,time,fd_hr,td_hr,avg_cr,rmssd,sdnn,f1,f2,f3,f4,f5):
    
    df_feat=pd.DataFrame()
    
    df_feat['Pulse_Type']=pd.Series(pulse)
    df_feat['Name']=pd.Series(name)
    df_feat['Day']=pd.Series(day)
    df_feat['Time']=pd.Series(time)
    
    df_feat['FD_HR'+pulse]=pd.Series(fd_hr)
    df_feat['TD_HR'+pulse]=pd.Series(td_hr)
    df_feat['Average_Correlation'+pulse]=pd.Series(avg_cr)
    df_feat['RMSSD'+pulse]=pd.Series(rmssd)
    df_feat['SDNN'+pulse]=pd.Series(sdnn)
    df_feat['Base_triangle'+pulse]=pd.Series(np.mean(f1))
    df_feat['Auc'+pulse]=pd.Series(np.mean(f2))
    df_feat['Amplitude'+pulse]=pd.Series(np.mean(f3))
    df_feat['Systolic_time'+pulse]=pd.Series(np.mean(f4))
    df_feat['Systolic_slope'+pulse]=pd.Series(np.mean(f5))
    return df_feat       
