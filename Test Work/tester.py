import os
from sklearn.externals import joblib
from ceps import read_ceps, create_ceps_test, read_ceps_test
from utils import GENRE_LIST, GENRE_DIR
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#          Please run the classifier script first
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def test_model_on_single_file(test_file):
    clf = joblib.load('saved_model/model_ceps.pkl')
    X, y = read_ceps_test(create_ceps_test(test_file)+".npy")
    probs = clf.predict_proba(X)
    print "\t".join(str(x) for x in traverse)
    print "\t".join(str("%.3f" % x) for x in probs[0])
    probs=probs[0]
    max_prob = max(probs)
    for i,j in enumerate(probs):
        if probs[i] == max_prob:
            max_prob_index=i
    
    print max_prob_index
    predicted_genre = traverse[max_prob_index]
    print "\n\npredicted genre = ",predicted_genre
    return predicted_genre

if __name__ == "__main__":
    
    global traverse
    for subdir, dirs, files in os.walk(GENRE_DIR):
        traverse = list(set(dirs).intersection(set(GENRE_LIST)))
        break
    
    print "\nDEBUG-Printing Traverse:"
    print traverse
    print "\n"
    

    test_file = "test_songs/beethoven-symph5-clip.wav"
    test_file2 = "test_songs/one.wav"
    test_file3 = "test_songs/michael-jackson-thriller.wav"
    # should predict genre as "ROCK"
    predicted_genre = test_model_on_single_file(test_file)
    predicted_genre = test_model_on_single_file(test_file2)
    predicted_genre = test_model_on_single_file(test_file3)
    
