import pandas as pd

# Visualizador de ecg
# Autor: V yanez

import wfdb
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
import os
import pandas as pd

# autoencoder post filtro
# gráfico de derivación para detección de ruido (similar a compresores)
# paper de cardiología para entender el problema.

# filtro de paso bajo Butterworth bidireccional
def butter_lowpass_filter(data, cutoff=1, fs=250, order=2):
    from scipy.signal import butter, filtfilt
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Función que busca todos los nombres únicos de archivos en un directorio sin su extrensión
def get_files(path):
    files = []
    for file in os.listdir(path):
        if file.endswith(".hea"):
            files.append(file[:-4])
    return files

# Función que genera la grafica de un archivo ecg
def genera_ecg_graf(file):
    # lee archivo .hea
    record = wfdb.rdheader('data/training/'+file)
    # carga archivo .mat (tiene las señales)
    mat_data = loadmat('data/training/'+file+'.mat')
    # claves del archivo .mat para saber como se llaman las señales
    #print(signals.keys())
    
    signals = mat_data['val']

    # recorta y deja sólo los últimos 10 segundos de señal
    signals = signals[:, -record.fs*10:]

    # aplica filtro de paso bajo (sólo para ECG)
    #filtered_signal = np.array([butter_lowpass_filter(signals[i, :]) for i in range(signals.shape[0])])
    #baseline_corrected_signal = signals - filtered_signal

    #grafica las señales ecg
    plt.figure(figsize=(12, 6))
    for i in range(len(record.sig_name)):
        plt.subplot(len(record.sig_name), 1, i+1)
        plt.plot(signals[i, :], label=f'Señal: {record.sig_name[i]}')
        plt.xlabel('Muestras')
        plt.ylabel(record.units[i])
        plt.legend()
    #agregar comentarios
    plt.suptitle(record.comments[0] + ' - ' + record.comments[1])
    # genera jpg
    plt.savefig('data/imgs/'+file+'.jpg')
    plt.close()
    



# Función que recorre todos los archivos de un directorio y genera las graficas de los ecg
def recorre_ecg_data(files):
    for file in files:
        print('Generando grafica de: ', file)
        # Genera la configuración de la grafica
        genera_ecg_graf(file)


def main():
    path='data/training/'
    files = get_files(path)
    recorre_ecg_data(files)
    
main()