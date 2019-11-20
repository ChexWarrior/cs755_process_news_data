import pandas as pd
import numpy as np
import keras
import sklearn
import pickle

from sklearn.model_selection import train_test_split
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
        title = str(row[1]['title'])
        title = title.replace('\xa0', ' ')

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

# Save labels and text
with open('data', 'wb') as f:
  pickle.dump(all_words, f)

with open('labels', 'wb') as f:
  pickle.dump(labels, f)
