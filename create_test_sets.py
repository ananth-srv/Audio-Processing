import scipy.io.wavfile as wavfile
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
import string

data = []
label = []
counter = 0
word_lexicon = []

def process_data(x):
    global data
    global counter
    filename = "D:/Docs/Audio/Movies/Autograph/" + x + ".wav"
    rate, wave_data = wavfile.read(filename)
    wave_data.shape = (1, 2 * len(wave_data))
    zerodata = np.zeros([1, 200000 - np.shape(wave_data)[1]])
    wave_data = np.append(wave_data, zerodata, axis=1)
    if counter == 0:
        data = wave_data
    else:
        data = np.append(data,wave_data, axis=0)

    counter = 1

def create_label_data(z):
    global label
    global counter
    global word_lexicon
    curr_label = np.zeros([1,len(word_lexicon)])
    z = z.translate({ord(c): None for c in string.punctuation})
    words = word_tokenize(z.lower())
    for i in words:
        if i.lower() in word_lexicon:
            index_value = np.where(word_lexicon == i)
            curr_label[0,index_value] = curr_label[0,index_value] + 1
    if counter == 0:
        label = curr_label
    else:
        label = np.append(label,curr_label,axis=0)

    counter = 1


def read_audio_file():
    global counter
    global word_lexicon
    input_data = pd.read_csv("D:/Docs/Audio/Movies/Autograph/test.csv",
                             dtype={
                            'file': np.string_,
                            'text': np.string_})

    for i in input_data['file']:
        print(i)
        process_data(i)

    counter = 0
    word_lexicon = np.genfromtxt("D:/Docs/Audio/Movies/Autograph/save_lexicon.txt", dtype=str)

    for i in input_data['text']:
        create_label_data(i)

    print(data)
    print(word_lexicon)
    print(label)

read_audio_file()
np.savetxt("D:/Docs/Audio/Movies/Autograph/test_data.txt", data, fmt='%d')
np.savetxt("D:/Docs/Audio/Movies/Autograph/test_label.txt", label, fmt='%d')
