import pandas as pd
import numpy as np
import keras
import sklearn
import pickle

from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

# Load Data
with open('data', 'rb') as f:
  all_words = pickle.load(f)

with open('labels', 'rb') as f:
  labels = pickle.load(f)

# Determine max length
max_title_length = -1
for w in all_words:
  if (len(w) > max_title_length):
      max_title_length = len(w)

# Tokenize
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_words)
sequences = tokenizer.texts_to_sequences(all_words)

word_index = tokenizer.word_index
print('Word_index' + str(word_index))

data = pad_sequences(sequences, maxlen=max_title_length)

X_train, X_test_, y_train, y_test = train_test_split(data, labels)

embeddings_index = {}
f = open('./glove.6B.50d.txt')
for line in f:
  values = line.split()
  word = values[0]
  coefs = np.asarray(values[1:], dtype='float32')
  embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))

embedding_matrix = np.zeros((len(word_index) + 1, 50))

for word, i in word_index.items():
  embedding_vector = embeddings_index.get(word)
  if embedding_vector is not None:
    embedding_matrix[i] = embedding_vector
