import scipy
import numpy as np
import os
import scipy.io.wavfile
import glob #used to iterate through a directory
from scikits.talkbox.features import mfcc

#edit these variables
PATH = 'C:/Users/Henry/Documents/AxonRadioMiscStorage/genres/**/*.wav'
GENRE_DIR = "C:/Users/Henry/Documents/AxonRadioMiscStorage/genres/"

#blow is an enumerate list which is used to label the genres in our dataset folder, blues = 0, classical = 1, .., rock = 9
#GENRE_LIST = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
GENRE_LIST = ["classical", "jazz", "country", "pop", "rock", "metal"]

def write_ceps(ceps, fname):
    """
    Write the MFCC to separate files to speed up processing.
    """
    base_fname, ext = os.path.splitext(fname)
    data_fname = base_fname + ".ceps"
    np.save(data_fname, ceps)
    print("Written %s"%data_fname)


def create_ceps(fname):
    sample_rate, X = scipy.io.wavfile.read(fname)

    ceps, mspec, spec = mfcc(X)
    write_ceps(ceps, fname)

def read_ceps(genre_list, base_dir=GENRE_DIR):
    X = []
    y = []
    for label, genre in enumerate(genre_list):
        for fname in glob.glob(os.path.join(base_dir, genre, "*.ceps.npy")):
            ceps = np.load(fname)
            num_ceps = len(ceps)
            X.append(
                np.mean(ceps[int(num_ceps / 10):int(num_ceps * 9 / 10)], axis=0))
            y.append(label)

    return np.array(X), np.array(y)

def create_ceps_glob(path):
    """creates MFCC files for all .wav files in a glob.glob directory parameter.
    \nExample: 'example/\\*\\*/\\*.wav' goes through all folders in example using \\*\\*
     and grabs every .wav in those folders"""
    for fname in glob.glob(path):
        create_ceps(fname)

#uncomment below to use create_ceps_glob(path)
#create_ceps_blob(PATH)

#uncomment below to print the read_ceps arrays on the terminal
#print read_ceps(GENRE_LIST)

#change to if __name__ == "__main__" later