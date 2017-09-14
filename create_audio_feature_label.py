import scipy.io.wavfile as wavfile
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
import string

data = []
label = []
word_lexicon = []
counter = 0


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


def create_lexicon(y):
    global word_lexicon
    global counter
    y = y.translate({ord(c): None for c in string.punctuation})
    words = word_tokenize(y.lower())
    if counter == 0:
        word_lexicon = words
    else:
        print(word_lexicon)
        for i in words:
            if i not in word_lexicon:
                print(i)
                word_lexicon = np.append(word_lexicon, i)
    counter = 1


def create_label_data(z):
    global label
    global counter
    l = 1
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
    input_data = pd.read_csv("D:/Docs/Audio/Movies/Autograph/data.csv",
                             dtype={
                            'file': np.string_,
                            'text': np.string_})

    for i in input_data['file'][:25]:
        print(i)
        process_data(i)

    counter = 0

    for i in input_data['text'][:25]:
        create_lexicon(i)

    counter = 0

    for i in input_data['text'][:25]:
        create_label_data(i)

    print(data)
    print(word_lexicon)
    print(label)

read_audio_file()
np.savetxt("D:/Docs/Audio/Movies/Autograph/save25_data.txt", data, fmt='%d')
np.savetxt("D:/Docs/Audio/Movies/Autograph/save25_label.txt", label, fmt='%d')
np.savetxt("D:/Docs/Audio/Movies/Autograph/save25_lexicon.txt", word_lexicon, fmt="%s")
