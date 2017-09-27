import scipy
import numpy as np
import os
from matplotlib.pyplot import specgram
import matplotlib.pyplot as plt
import scipy.io.wavfile
import glob #used to iterate through a directory

PATH='C:/Users/Henry/Documents/AxonRadioMiscStorage/genres_converted/**/*.wav'

#enumerate list which is used to label the genres in our dataset folder, blues = 0, classical = 1, .., rock = 9
genre_list = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

#the directory to our folder containing the genres
GENRE_DIR = "C:/Users/Henry/Documents/AxonRadioMiscStorage/genres_converted/"

def create_fft(fname):
    """creates an FFT from a .wav file given as its parameter then saves it in the same folder as the .wav as a .fft.npy for later reading"""
    sample_rate, X = scipy.io.wavfile.read(fname)
    fft_features = abs(scipy.fft(X)[:1000])
    base_fname, ext = os.path.splitext(fname)
    data_fname = base_fname + ".fft"
    np.save(data_fname, fft_features)

def read_fft(genre_list, base_dir=GENRE_DIR):
    """iterates through the GENRE_DIR directory going through all our genre folders
     and adding the FFT data to the x array and its genre (0-9) in the y array"""
    X = []
    Y = []
    for label, genre in enumerate(genre_list):
        genre_dir = os.path.join(base_dir, genre, "*.fft.npy")
        file_list = glob.glob(genre_dir)
        for fname in file_list:
            fft_features = np.load(fname)

            X.append(fft_features[:1000])
            Y.append(label)

    return np.array(X), np.array(Y)

def plot_wav_fft(wav_filename, desc=None):
    """creates an FFT from a .wav file and plots the sample rate of the file in one plot and then the FFT plot in a seperate plot."""
    plt.clf()
    plt.figure(num=None, figsize=(6, 4))
    sample_rate, X = scipy.io.wavfile.read(wav_filename)
    spectrum = np.fft.fft(X)
    freq = np.fft.fftfreq(len(X), 1.0 / sample_rate)

    plt.subplot(211)
    num_samples = 2000.0 #changed from 200.0 to 2000.0 , from 0.008 seconds to 0.08
    plt.xlim(0, num_samples / sample_rate)
    plt.xlabel("time [s]")
    plt.title(desc or wav_filename)
    plt.plot(np.arange(num_samples) / sample_rate, X[:num_samples])
    plt.grid(True)

    plt.subplot(212)
    plt.xlim(0, 5000)
    plt.xlabel("frequency [Hz]")
    plt.xticks(np.arange(5) * 1000)
    if desc:
        desc = desc.strip()
        fft_desc = desc[0].lower() + desc[1:]
    else:
        fft_desc = wav_filename
    plt.title("FFT of %s" % fft_desc)
    plt.plot(freq, abs(spectrum), linewidth=5)
    plt.grid(True)

    plt.tight_layout()

    rel_filename = os.path.split(wav_filename)[1]
    plt.savefig("%s_wav_fft.png" % os.path.splitext(rel_filename)[0],
                bbox_inches='tight')

    plt.show()

def plot_wav_fft_demo():
    """demo function to test the plot_wav_fft() function where you choose which files to plot"""
    plot_wav_fft("C:/Users/Henry/Documents/AxonRadioMiscStorage/genres_converted/blues/blues.00000.wav", "blues.00000.wav")
    plot_wav_fft("C:/Users/Henry/Documents/AxonRadioMiscStorage/genres_converted/pop/pop.00000.wav", "pop.00000.wav")
    plot_wav_fft("C:/Users/Henry/Documents/AxonRadioMiscStorage/genres_converted/metal/metal.00000.wav", "metal.00000.wav")

def read_fft_demo():
    """demo funciton of read_fft()
    \nsaving the arrays returned by read_fft(genre_list) into the variables testX and testY"""
    testX, testY = read_fft(genre_list)
    return(testX,testY)

def create_fft_directory(path):
    """creates ffts for all .wav files in a glob.glob directory parameter.
    \nExample: 'example/\\*\\*/\\*.wav' goes through all folders in example using \\*\\*
     and grabs every .wav in those folders"""
    for fname in glob.glob(path):
        create_fft(fname)



print read_fft_demo()

#plot_wav_fft_demo()
