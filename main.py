import pandas as pd
import numpy as np
import keras

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

def get_csv_data(file_path):
    return pd.read_csv(file_path, usecols=['title', 'publication'], dtype={'title': str , 'publication': str})

max_title_length = -1
data_by_publication = dict()
data_paths = [
    './articles1.csv',
    './articles2.csv',
    './articles3.csv',
]

for path in data_paths:
    data = get_csv_data(path)

    for row in data.iterrows():
        pub = row[1]['publication']
        title = row[1]['title']

        if pub in data_by_publication:
            data_by_publication[pub].append(title)
        else:
            data_by_publication[pub] = [title]

for pub in data_by_publication:
    print(str(len(data_by_publication[pub])) + ' titles from ' + pub)

# Determine label of titles by source
bias_ratings = {
  'New York Times': 'left',
  'Breitbart': 'right',
  'CNN': 'left',
  'Business Insider': 'center',
  'Atlantic': 'left',
  'Fox News': 'right',
  'Talking Points Memo': 'unknown',
  'Buzzfeed News': 'left',
  'National Review': 'right',
  'New York Post': 'right',
  'Guardian': 'left',
  'NPR': 'center',
  'Reuters': 'center',
  'Vox': 'left',
  'Washington Post': 'left',
}

# Concatenate left/right sources
left_publications = []
right_publications = []
for pub in data_by_publication:
    if bias_ratings[pub] == 'left':
        left_publications.extend(data_by_publication[pub])

    if bias_ratings[pub] == 'right':
        right_publications.extend(data_by_publication[pub])

num_right = len(right_publications)
num_left = len(left_publications)

print('Totals before evening out...')
print('Total of ' + str(num_right) + ' right articles!')
print('Total of ' + str(num_left) + ' left articles!')

if (num_left > num_right):
    left_publications = left_publications[:num_right]
elif (num_right > num_left):
    right_publications = right_publications[:num_left]

num_right = len(right_publications)
num_left = len(left_publications)

print('Total of ' + str(num_right) + ' right articles!')
print('Total of ' + str(num_left) + ' left articles!')

# Combine data
all_titles = left_publications + right_publications
all_words = [s.split(" ") for s in all_titles]

# Create labels
# 0 left, 1 is right
labels = [[0,1]] * num_left
labels.extend([[1,0]] * num_right)

# Determine max length
for w in all_words:
    if (len(w) > max_title_length):
        max_title_length = len(w)

print('Max Title Length: ' + str(max_title_length))

# Tokenize
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_words)
sequences = tokenizer.texts_to_sequences(all_words)

word_index = tokenizer.word_index
data = pad_sequences(sequences, maxlen=max_title_length)

np.savetxt(fname='data.csv', delimiter=',', X=data)
np.savetxt(fname='labels.csv', delimiter=',', X=np.asarray(labels))
