import matplotlib.pyplot as plt
import numpy as np
import scipy
from csi_reader_with_args import process_data

args, amplitudes, phases = process_data()

data = np.asarray(amplitudes)
subcarrier = 44
print(data)
csi_data = data[:, subcarrier]

fs = 4

# 傅里叶变换
N = len(csi_data)
yf = scipy.fftpack.fft(csi_data)
xf = np.fft.fftfreq(N, 1/fs)
 
# 绘制频谱图
plt.figure()
plt.plot(xf[:N//2], 2.0/N * np.abs(yf[:N//2]))
plt.title('Original Signal Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()