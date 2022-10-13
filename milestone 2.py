import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft
from scipy.signal import find_peaks

t = np.linspace(0,3,12*1024)

l = [130.81, 261.63, 329.63, 261.63, 349.23, 261.63, 329.63]

r = [261.63, 261.63, 392, 392, 440, 440, 392]


start = [0, 0.45, 0.9, 1.35, 1.8, 2.25, 2.7]
duration = [0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.3]

def u(t):
    return 1*(t>=0)

x = 0

#the original signal without noise in time domain
for i in range(0,7):
    x+=(np.sin(2*np.pi*l[i]*t) + np.sin(2*np.pi*r[i]*t))*(u(t-start[i])-u(t-start[i]-duration[i]))

plt.figure()
plt.plot(t,x)


N = 3*1024
f = np.linspace(0,512,int(N/2))

#converting the original signal to frequency domain
x_f = fft(x)
x_f = 2/N*np.abs(x_f [0:np.int(N/2)])

plt.figure()
plt.plot(f,x_f)

#generating two random numbers
fn1 = np.random.randint(0, 512, 1)
fn2 = np.random.randint(0, 512, 1)

#generating noise from two random numbers in time domain
noise = np.sin(2*np.pi*fn1*t) + np.sin(2*np.pi*fn2*t)

#the original signal and noise added together in time domain
x_noise = x + noise
plt.figure()
plt.plot(t,x_noise)

#converting the signal with noise to frequency domain 
X_n = fft(x_noise) 
X_n = 2/N*np.abs(X_n [0:np.int(N/2)])
plt.figure()
plt.plot(f,X_n)

#using find_peaks to find the two frequencies with highest amplitudes, which are the randomly generated noise
peaks,_ = find_peaks(X_n, height=[3,10])

#saving these two frequencies in variables; time domain
fn1_new = peaks[0]/3
fn2_new = peaks[1]/3


#generating new noise, which should be exactly the same as the variable noise; time domaim
new_noise =  np.sin(2*np.pi*fn1_new*t) + np.sin(2*np.pi*fn2_new*t) 

#removing the newly found noise from the signal which contains the song and noise; time domain
x_filtered = x_noise - new_noise
plt.figure()
plt.plot(t,x_filtered)

#transforming the filtered signal to frequency domain
X_filtered = fft(x_filtered)
X_filtered = 2/N*np.abs(X_filtered [0:np.int(N/2)])
plt.figure()
plt.plot(f,X_filtered)

sd.play(x_filtered,3*1024)