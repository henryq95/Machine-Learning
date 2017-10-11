import scipy
import numpy as np
import os
import scipy.io.wavfile
import glob #used to iterate through a directory
from scikits.talkbox.features import mfcc

#edit these variables
PATH = 'C:/Users/Henry/Documents/AxonRadioMiscStorage/genres/**/*.wav'
GENRE_DIR = "C:/Users/Henry/Documents/AxonRadioMiscStorage/genres/"

#below is an enumerate list which is used to label the genres in our dataset folder, blues = 0, classical = 1, .., rock = 9
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
    """
    Creates the MFCC features.
    """
    sample_rate, X = scipy.io.wavfile.read(fname)

    ceps, mspec, spec = mfcc(X)
    write_ceps(ceps, fname)

def read_ceps(genre_list, base_dir=GENRE_DIR):
    """
        Reads the MFCC features from disk and
        return them in a numpy array.
    """
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

def create_ceps_test(fname):
    """
        Creates the MFCC features from the test files,
        saves them to disk, and returns the saved file name.
    """
    sample_rate, X = scipy.io.wavfile.read(fname)
    X[X==0]=1
    np.nan_to_num(X)
    ceps, mspec, spec = mfcc(X)
    base_fname, ext = os.path.splitext(fname)
    data_fname = base_fname + ".ceps"
    np.save(data_fname, ceps)
    print "Written ", data_fname
    return data_fname


def read_ceps_test(test_file):
    """
        Reads the MFCC features from disk and
        returns them in a numpy array.
    """
    X = []
    y = []
    ceps = np.load(test_file)
    num_ceps = len(ceps)
    X.append(np.mean(ceps[int(num_ceps / 10):int(num_ceps * 9 / 10)], axis=0))
    return np.array(X), np.array(y)



#if this file is executed first, it executes create_ceps_glob
if __name__ == "__main__":
    create_ceps_glob(PATH)


#uncomment below to print the read_ceps arrays on the terminal
#print read_ceps(GENRE_LIST)
