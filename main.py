from sklearn.feature_extraction.text import TfidfVectorizer

from tensorflow.keras.callbacks import LambdaCallback
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.optimizers import Adamax
from tensorflow.keras.optimizers import RMSprop

import numpy as np
import pandas as pd
import random
import requests
import sys
import re



# Bring in the data. Right now I'm just doing train. Will add validate later.
lines = ""
with open('train.txt', 'r', encoding='iso-8859-1') as dialogues:
    for line in dialogues:
        lines += line


# Original words will be the y. They retain punctuation and capitalization.
orig_words = lines.replace("\n", " \n ").replace(" -", "-").split(" ")
orig_words =  list(filter(lambda a: a != '', orig_words))


# New words will be the X. They don't have capitalization and punctuation.
new_words = []
for word in orig_words:
    w = re.sub(r'[^\w\s]','',word) #remove everything except words, space
    w = re.sub(r'\_','',w)          # And underscore
    new_words.append(w.lower())


# Create Encoder/Decoder
text = orig_words + new_words
text.append('')

words = sorted(list(set(text)))
word_int = dict((c, i) for i, c in enumerate(words))
int_word = dict((i, c) for i, c in enumerate(words))


# Create the X and y more formally.
maxlen = 11

sentences = [] #X
next_words = [] #Y

maxlen = 11
contexts = []
preds = []


# This creates chunks that are 11 tokens long with the 
# middle token being the target word. 
for i in range(len(orig_words)):
    if i == 0:
        x1 = [''] * 5
        x2 = [new_words[0]]
        x3 = new_words[1:6]
        sentences.append(x1 + x2 + x3)
        next_words.append(orig_words[i])
    
    elif i < 5:
        x1 = [''] * (5-i)
        x2 = new_words[:i]
        x3 = new_words[i: i+6]
        sentences.append(x1 + x2 + x3)
        next_words.append(orig_words[i])

    elif i == len(orig_words):
        x1 = new_words[i-5:]
        x2 = [''] * 5
        sentences.append(x1 + x2)
        next_words.append(orig_words[i])

    elif i > len(orig_words) - 6:
        x1 = new_words[i-5:]
        x2 = [''] * (6 - (len(orig_words) - i))
        sentences.append(x1 + x2)
        next_words.append(orig_words[i])
    
    else:
        sentences.append(new_words[i-5: i+6])
        next_words.append(orig_words[i])

for i in range(0, len(text)- maxlen):
    sentences.append(text[i: i + maxlen])
    next_words.append(text[i + maxlen])

# Specify X and y
x = np.zeros((len(sentences), maxlen, len(words)), dtype=np.bool)
y = np.zeros((len(sentences), len(words)), dtype=np.bool)

for i, sentence in enumerate(sentences):
    for t, word in enumerate(sentence):
        x[i, t, word_int[word]] = 1
    y[i, word_int[next_words[i]]] = 1

# Early Stopping Requirements
stop = EarlyStopping(monitor='loss', min_delta=0.05, patience=2, mode='auto')

# Build Model
model = Sequential()
model.add(LSTM(300, input_shape=(maxlen, len(words))))
model.add(Dense(900, activation='relu'))
model.add(Dense(len(words), activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adamax')

# Fit Model
model.fit(x, y,
        batch_size=32,
        epochs=200, 
        callbacks=[stop])

# Save Model
model.save(f'punctuation')



def gen_data(sentences):
    """A function to generate predictions for the sixth word
        of every chunk in sentences and then returns them
        as a list of words."""

    # With more time I would refine it to make it able to handle one
    # large string that's a whole document and then return the whole
    # document with capitalization and punctuation fixed.

    data = []
    for sentence in sentences:
        senten = sentence.split(" ")
        x_pred = np.zeros((1, maxlen, len(words)))
        for t, word in enumerate(senten):
            x_pred[0, t, word_int[word]] = 1
        preds = model.predict(x_pred, verbose=0)[0]
        data.append(int_word[np.argmax(preds)])

    return data

# This is just an example of a few chunks whose sixth words
# make at least part of a sentence.
sentences = ['thats the kind of guy she likes pretty ones \n who', 'the kind of guy she likes pretty ones \n who knows', 'kind of guy she likes pretty ones \n who knows all', 'of guy she likes pretty ones \n who knows all ive', 'guy she likes pretty ones \n who knows all ive ever', 'she likes pretty ones \n who knows all ive ever heard', 'likes pretty ones \n who knows all ive ever heard her', 'pretty ones \n who knows all ive ever heard her say', 'ones \n who knows all ive ever heard her say is', '\n who knows all ive ever heard her say is that']
print(gen_data(sentences))