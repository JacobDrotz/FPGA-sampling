import itertools
import logging
import socket
import sys
import struct
import time 
from ctypes import Structure, c_byte, c_int32, sizeof
from ast import For
import numpy as np
import math
import struct
import matplotlib.pyplot as plt
from pathlib import Path
from ctypes import Structure, c_byte, c_int32, sizeof
#import config
import os
from scipy.io.wavfile import write
from scipy import signal 
from scipy.signal import butter, filtfilt,correlate,chirp,welch,periodogram
# This scripts listen on an port and collects array samples and then plots the graphs direcly!
# Enter a filename and how long you want to record.
# Pick a horizontal line or a vertical line.
# the plotted graphs will show
# to make a new recording simply close all the graphs and a new session is started. 



def collect_samples(filename,recordTime):
   # NOTE: Check if big-endian or little-endian as this is often flipped
   # use:
   # from ctypes import LittleEndianStructure, BigEndianStructure
   # and replace Structure with LittleEndianStructure or BigEndianStructure to get the right one.
   class Data(Structure):
      _fields_ = [
         ("arrayId", c_int32),  
         ("protocolVer", c_int32),  # The data we care about
         ("frequency", c_int32),
         ("sampelCounter", c_int32),
         ("mic_1", c_int32),
         ("mic_2", c_int32),
         ("mic_3", c_int32),
         ("mic_4", c_int32),
         ("mic_5", c_int32),
         ("mic_6", c_int32),
         ("mic_7", c_int32),
         ("mic_8", c_int32),
         ("mic_9", c_int32),
         ("mic_10", c_int32),
         ("mic_11", c_int32),
         ("mic_12", c_int32),
         ("mic_13", c_int32),
         ("mic_14", c_int32),
         ("mic_15", c_int32),
         ("mic_16", c_int32),
         ("mic_17", c_int32),
         ("mic_18", c_int32),
         ("mic_19", c_int32),
         ("mic_20", c_int32),
         ("mic_21", c_int32),
         ("mic_22", c_int32),
         ("mic_23", c_int32),
         ("mic_24", c_int32),
         ("mic_25", c_int32),
         ("mic_26", c_int32),
         ("mic_27", c_int32),
         ("mic_28", c_int32),
         ("mic_29", c_int32),
         ("mic_30", c_int32),
         ("mic_31", c_int32),
         ("mic_32", c_int32),
         ("mic_33", c_int32),
         ("mic_34", c_int32),
         ("mic_35", c_int32),
         ("mic_36", c_int32),
         ("mic_37", c_int32),
         ("mic_38", c_int32),
         ("mic_39", c_int32),
         ("mic_40", c_int32),
         ("mic_41", c_int32),
         ("mic_42", c_int32),
         ("mic_43", c_int32),
         ("mic_44", c_int32),
         ("mic_45", c_int32),
         ("mic_46", c_int32),
         ("mic_47", c_int32),
         ("mic_48", c_int32),
         ("mic_49", c_int32),
         ("mic_50", c_int32),
         ("mic_51", c_int32),
         ("mic_52", c_int32),
         ("mic_53", c_int32),
         ("mic_54", c_int32),
         ("mic_55", c_int32),
         ("mic_56", c_int32),
         ("mic_57", c_int32),
         ("mic_58", c_int32),
         ("mic_59", c_int32),
         ("mic_60", c_int32),
         ("mic_61", c_int32),
         ("mic_62", c_int32),
         ("mic_63", c_int32),
         ("mic_64", c_int32),          
      ]
   UDP_IP = "0.0.0.0"
   UDP_PORT = 21844

   
   t_end = time.time()+int(recordTime)


   """Receive packages forever"""
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   sock.bind((UDP_IP, UDP_PORT))

   # itertools.count() is a generator that counts up forever.
   # same as while True with the added benefit of keeping track of the number of iterations.
   # Can be converted to a while True if count is unused.
   with open(filename, "wb") as f:

      #for count in itertools.count():
      while time.time()<t_end:
         data = sock.recv(sizeof(Data))
         
         d = Data.from_buffer_copy(data)
         f.write(d)
   f.close
   sys.stdout.flush()

def print_analysis(fileChooser):


   def load_data_FPGA():
      #   FUNCTION TO LOAD DATA FROM .BIN FILE INTO NUMPY ARRAY 
      #   (RECORDED BY FPGA)

      ROOT = os.getcwd()
      path = Path(ROOT + "/"+fileChooser)
   
      data = np.fromfile(path,dtype=c_int32,count=-1,offset=0) #Read the whole file
      data2D = data.reshape(-1,68)  # reshapes into a Numpy array which is N*68 in dimensions
      

      
     
      ## Data2D holds all information from the file.
      ## Data2D[n][0] = array id
      ## Data2D[n][1] = protocol version
      ## Data2D[n][2] = frequency
      ## Data2D[n][3] = array sample counter
      ## Data2D[n][4] to  Data2D[n][67] = is microphone 1 to 64

      

      micData = data2D[:,4:] #An array with only mic data. i.e removes (Array id, protocol version, freq and counter)
      f_sampling = np.fromfile(path,dtype=c_int32,count=1,offset=8) # get sampling frequency from the file
      #f_sampling = 10000
      return micData, int(f_sampling),fileChooser

   def main():
      recording_device = 'FPGA' # choose between 'FPGA' and 'BB' (BeagelBone) 
      
      # Load data from .BIN
      if recording_device == 'FPGA':
         data,fs,fileChooser = load_data_FPGA()
      #total_samples = len(data[:,0])          # Total number of samples
      #initial_data = data[0:initial_samples,] # takes out initial samples of signals 

      print("################# ANALYSE OF "+ fileChooser+" #################")
      print("\n")
      print('sample frequency: '+ str(int(fs)))

      staring_point = 1000                #default = 1000

      if recording_device == 'FPGA':
         ok_data = data[staring_point:,]  # all data is ok

      return ok_data
   
   ok_data = main()
   return ok_data

def tukey (v, size):  ## Creates a ramp in the end of the generated chirp, to avoid side lobes 
    if len(v) < 2*size:
        raise ValueError ("Tukey window size too big for array")
    tuk = 0.5 * (1.0 - np.cos (np.pi * np.arange(size) / size))
    v[0:size] *= tuk   # ADD his line for curve at the beginning aswell
    v[-size:] *= tuk[::-1]
    
    return v

def generate_chirp(start_f,stop_f,T,fs):
   start_f=start_f         #Start frequency
   stop_f=stop_f      #Stop frequency   
   T=T               #Time interval
   fs=fs          #sample rate assume 4*highest frecuency is enough
   N = fs*T

   t = np.linspace(0, T, int(T * fs), endpoint=False)
   t_space = 1/fs

   

   #normalisation factor used for inverse filter/matched filter
    #Below: sine and cos only represents the signals start phase.  try and use differen "chirp_signal"

    
   #  _______________________________Mark method_1_____________________________________ 
        # sine lin
   #chirp_signal = chirp(t, f0=start_f, t1=T, f1=stop_f, method='linear',phi=-90, vertex_zero=True ) 
        # sine log       
   #chirp_signal = signal.chirp(t, f0=start_f, t1=T, f1=stop_f, method='logarithmic',phi=-90, vertex_zero=True )   
        
        # cos lin
   #chirp_signal= chirp(t, f0=start_f, t1=T, f1=stop_f, method='linear', phi=0, vertex_zero=True) 
        # cos log         
   #chirp_signal = chirp(t, f0=start_f, t1=T, f1=stop_f, method='logarithmic',phi=-90, vertex_zero=True )  
   #_________________________________________________________________________________
   
   
   
   #_______________________________linspace method_2__________________________________    
        #Linear sine chirp 
   #chirp_signal = np.sin(2 * np.pi * np.linspace(start_f, stop_f, N) * (t**2/2))   # according to farina
   #chirp_signal = np.sin(2 * np.pi * np.linspace(start_f, stop_f, N) * t**2)   # acording to random stackoverflow                                                                      
        #logaritmic sine chirp
   #chirp_signal = np.sin(2 * np.pi * np.logspace(np.log10(start_f), np.log10(stop_f), N))
   #________________________________________________________________________________
   

   #_________________________________Farina formula_________________________________ 
         #Linear   BAD IN CURRENT STATE
   #chirp_signal = np.sin(start_f*t + ((stop_f-start_f)/2)*((t**2)/2))

         #logarithmic  BAD IN CURRENT STATE
   #chirp_signal = np.sin(((np.pi*2*start_f*T)/(np.log(stop_f/start_f)))* (np.exp((t*np.log(stop_f/start_f))/T) -1 ))
   # Create the frequency vector
   
         #Modified Farina sweep   works ________________________________
   #L is used for the modified farina sweep
   L= (1/start_f)*((T*start_f)/(np.log(stop_f/start_f)))
   chirp_signal = np.sin(2*np.pi*start_f*L *(np.exp(t/L)-1))
   #_________________________________________________________________________________________________________
   
   
   #t = np.linspace(0, T, int(fs * T), endpoint=False)
   #chirp_signal = chirp(t, start_f, T, stop_f, method='logarithmic')
   
   #creates curve at the end of signal.
   TUKEY_SAMPLES = N //16  ## number of samples to create curve at the end of chirp
   chirp_signal = tukey(chirp_signal,TUKEY_SAMPLES)                                   #uncomment to ad tukey effect in the end.

   
   #normalize the generated chirp to fit a target 24-bit range
   #scaling_factor = 8388607 / np.max(np.abs(chirp_signal))
   #chirp_signal_scaled = np.round(chirp_signal * scaling_factor).astype(np.int32)
   
   max_amplitude = np.max(np.abs(chirp_signal))
   scaling_factor = (2**24 - 1) / max_amplitude
   chirp_signal_scaled = np.round(chirp_signal * scaling_factor).astype(np.int32)

   #converts to int16
   #chirp_signal_scaled = np.int16((chirp_signal / chirp_signal.max()) * 32767)   # normalized to fit targetet format for n bit use (2^(n)/2  -1) = 32767 for 16bit. #this value sets the amplitude.
   

   
   return chirp_signal_scaled

def create_sound_file(signal,fs,name):

   #converts to int16
   #signal = np.int16((signal / signal.max()) * 32767)   # normalized to fit targetet format for n bit use (2^(n)/2  -1) = 32767 for 16bit. #this value sets the amplitude.
   #signal = np.int32((signal / np.max(np.abs(signal))) * (2**23-1))  #24 bit 
   write(name,fs , signal)


def truncation(fft_IR):
   # Compute magnitude spectrum
   #mag_spec = np.abs(fft_IR)

   # Find the location of the largest peak in the impulse response
   max_index = np.argmax(np.abs(fft_IR))

# Extract a portion of the impulse response around the largest peak
   truncated_impulse_response = fft_IR[max_index-450:max_index+450]
  
   return truncated_impulse_response

#################################################################################################
if __name__ == '__main__':
   ### values used for generating the chirp
   start_f=1         #Start frequency
   stop_f=22000      #Stop frequency   
   T=2               #Time interval
   fs=48828          #sample rate assume 4*highest frecuency is enough  44100 is normal for audio recording, maybe match our SR?
   N = fs*T

   #names for the audio files
   #filename_pure_chip = "chirp.wav"
   file_name_recording = "recording_sim.wav"
   filename_pure_chip = "11k_scipy_chirp_log.wav"
   chirp_signal = generate_chirp(start_f,stop_f,T,fs)   #Generate chirp and its corresponding matched filter
   #create_sound_file(chirp_signal,fs,filename_pure_chip)

   


   #normalize to be able to create a audio file. same values is used here
   #chirp_signal = np.int16((chirp_signal / chirp_signal.max()) * 32767)   # normalized to fit targetet format for n bit use (2^(n)/2  -1) = 32767 for 16bit. #this value sets the amplitude.

   print("Enter a filename for the recording: ")
   fileChooser = input()
   print("enter referece_mic to calibrate according to the chirp")
   ref_microphone=input()
   ref_microphone=int(ref_microphone)-1
   print("enter mic to calibrate according to the chirp")
   other_microphone=input()
   other_microphone=int(other_microphone)-1
   #print("press ENTER to start")
   input("press ENTER to start")
   record_time=T
   #collect_samples(fileChooser,record_time)    #if you wish do use a pre-recorde file, have this line as a comment

   recording= print_analysis(fileChooser)    #Recording contains data from alla microphones, reference_microphone cointains data from selected mic
  
   #take out reference mic   
   ref_mic=recording[:,ref_microphone]             
   

   # Normalize the amplitude of the generated chirp
   chirp_signal = chirp_signal / np.max(np.abs(chirp_signal))
   chirp_signal *= np.max(np.abs(ref_mic))
   
   #create the matched filter version
   t = np.linspace(0, T, int(T * fs), endpoint=False)
   R = np.log(stop_f/start_f)
   k = np.exp(t*R/T)
   matched_filter =  chirp_signal[::-1]/k   #divide by k for constans FR for the matched filter

   
   fft_size = len(ref_mic) #

   #get IR and FR for reference mic
   ref_mic_IR_plot = np.convolve(ref_mic,matched_filter,mode='same')
   ref_mic_IR=truncation(ref_mic_IR_plot)
 

   # Normalize the signal
   #ref_mic_IR = ref_mic_IR / np.max(ref_mic_IR)
   #normalized_ref_mic_IR = 2 * (ref_mic_IR - ref_mic_IR.min()) / (ref_mic_IR.max() - ref_mic_IR.min()) - 1
   ref_mic_FR = np.fft.fft(ref_mic_IR,fft_size)

   #get IR and FR for chirp
   chirp_IR_plot = np.convolve(chirp_signal,matched_filter,mode='same')
   chirp_IR=truncation(chirp_IR_plot)

   #chirp_IR = 2 * (chirp_IR - chirp_IR.min()) / (chirp_IR.max() - chirp_IR.min()) - 1
   #chirp_IR = chirp_IR / np.max(chirp_IR)
   chirp_FR = np.fft.fft(chirp_signal,fft_size)
   #chirp_FR = np.abs(chirp_FR)

   samples_IR = np.arange(len(ref_mic))
   time = samples_IR / fs  # assuming sample_rate is known
   # Plot the chirp signal in the time domain
   plt.subplot(2,1,1)
   plt.plot(time, ref_mic_IR_plot)
   plt.xlabel('Time (s)')
   plt.ylabel('Amplitude')
   plt.title('Impulse response')
   
   samples_IR = np.arange(len(chirp_signal))
   time = samples_IR / fs  # assuming sample_rate is known
   # Plot the chirp signal in the time domain
   plt.subplot(2,1,2)
   plt.plot(time, chirp_IR_plot)
   plt.xlabel('Time (s)')
   plt.ylabel('Amplitude')
   plt.title('Impulse response')
   
   #_________________________________________________________________________________________________________________________
  


   #receive the frequency respons of the reference microphone   145476
   scaling_factor = ref_mic_FR/chirp_FR
   amp_scaling_factor = scaling_factor * np.exp(1j * np.zeros_like(scaling_factor))
   
   

   ref_mic_calibrated_fft = ref_mic_FR*amp_scaling_factor

   #go back into time-domain
   ref_mic_calibrated = np.fft.ifft(ref_mic_calibrated_fft,fft_size)
   
   ref_mic_error = ref_mic[0:fft_size] - ref_mic_calibrated

   # _____________plotting HeatMap__________________
    # Compute spectrogram
   f, t, Sxx = signal.spectrogram(ref_mic, fs=fs)
#
   #Plot heatmap
   fig, ax = plt.subplots()
   im = ax.pcolormesh(t, f, 10 * np.log10(Sxx), cmap='inferno', shading='auto')
   ax.set_xlabel('Time (s)')
   ax.set_ylabel('Frequency (Hz)')
   cbar = fig.colorbar(im)
   cbar.set_label('Power (dB)')
   plt.show()

 



   # Assume chirp is your chirp signal with N samples
   N = fft_size
   time = np.arange(N) / fs  # assuming sample_rate is known


   
   #____________________SPL_________________________#
   # Calculate the voltage from the raw data
   #sensitivity = -26 
   #spl = 20 * np.log10(np.abs(ref_mic) / (2**23 * 10**(sensitivity/20)))   #??????????????????

   #________________________________________________________________________________

   plt.subplot(3,1,1)
   plt.plot(time, ref_mic[0:fft_size],label="reference mic",color="green")
   plt.xlabel('Time (s)')
   plt.ylabel('Amplitude')
   plt.legend(loc='upper right')

   
   
   


      # Assume chirp is your chirp signal with N samples
   N = len(ref_mic_calibrated)
   time = np.arange(N) / fs  # assuming sample_rate is known

   plt.subplot(3,1,2)
   plt.plot(time, ref_mic_calibrated,label="calibrated mic",color="orange")
   plt.xlabel('Time (s)')
   plt.ylabel('Amplitude')
   plt.legend(loc='upper right')
   
   

   # Assume chirp is your chirp signal with N samples
   N = len(ref_mic_calibrated)
   time = np.arange(N) / fs  # assuming sample_rate is known

   #plt.subplot(4,1,4)
   #plt.plot(time, other_mic_error,color="red",label="deviation")
   #plt.xlabel('Time (s)')
   #plt.ylabel('Amplitude')
   #plt.title('deviation = before cal - after_cal')
   #plt.legend(loc='upper right')
   #plt.tight_layout()
   plt.show()


   ## Correct SPL value ## ___________________________________________________________________

   # ICS-52000 microphone Full-scale sensitivity (-26 dBFS/Pa)
   sensitivity = -26.0

   # Define the reference voltage and sound pressure level
   Vref = 1.0 # volt
   SPLref = 94.0 # dB SPL

   #  Load the microphone's output waveform from a WAV file
   waveform = ref_mic / (2 ** 24 -1)

   # Convert the waveform to RMS voltage
   Vrms = np.sqrt(np.mean(waveform ** 2))

   # Calculate the SPL value using the formula
   SPL = 20 * np.log10(Vrms / 0.0501187234) + SPLref

   # Print the calculated SPL value
   print('SPL ref mic: {:.2f} dB'.format(SPL))


   #  Load the microphone's output waveform from a WAV file
   waveform = ref_mic_calibrated.real/ (2 ** 24 -1)

   # Convert the waveform to RMS voltage
   Vrms = np.sqrt(np.mean(waveform ** 2))

   # Calculate the SPL value using the formula
   SPL = 20 * np.log10(Vrms / 0.0501187234) + SPLref

   # Print the calculated SPL value
   print('SPL after cal: {:.2f} dB'.format(SPL))
   #_________________________________________________________________________________________


   #____________________Plot frequency domain__________
   magnitude_other_mic_fft = np.abs(ref_mic_FR)
   magnitude_spectrum_other_mic_calibrated_fft = np.abs(ref_mic_calibrated_fft)
   magnitude_spectrum_other_mic_error = np.abs(np.fft.fft(ref_mic_error))

   
   chirp_FR = np.abs(chirp_FR)
   # Plot the chirp signal in the time domain
   # Plot the magnitude spectrum
   freqs = np.fft.fftfreq(fft_size, 1/fs)
   plt.plot(freqs[:fft_size//2], chirp_FR[:fft_size//2],label="Generated swept sine")
   plt.xlabel('Frequency (Hz)')
   plt.ylabel('Magnitude')
   plt.legend(loc='upper right')
   plt.show()

   
   # Plot the magnitude spectrum
   freqs = np.fft.fftfreq(fft_size, 1/fs)
   plt.plot(freqs[:fft_size//2], magnitude_other_mic_fft[:fft_size//2],label="Recorded swept sine")
   plt.xlabel('Frequency (Hz)')
   plt.ylabel('Magnitude')
   plt.legend(loc='upper right')

   ## Plot the magnitude spectrum
   #freqs = np.fft.fftfreq(fft_size, 1/fs)
   #plt.plot(freqs[:fft_size//2], magnitude_spectrum_other_mic_calibrated_fft[:fft_size//2],label="calibrated")
   #plt.xlabel('Frequency (Hz)')
   #plt.ylabel('Magnitude')
   #plt.legend(loc='upper right')
#
   ## Plot the magnitude spectrum
   #freqs = np.fft.fftfreq(fft_size, 1/fs)
   #plt.plot(freqs[:fft_size//2], magnitude_spectrum_other_mic_error[:fft_size//2], label="deviation")
   #plt.xlabel('Frequency (Hz)')
   #plt.ylabel('Magnitude')
   #plt.legend(loc='upper right')
   #plt.tight_layout()
   plt.show()


  