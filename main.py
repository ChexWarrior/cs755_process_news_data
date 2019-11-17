import pandas as pd
import numpy as np

def get_csv_data(file_path):
    return pd.read_csv(file_path, usecols=['title', 'publication'], dtype={'title': str , 'publication': str})

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

# Concatentate left/right sources
left_publications = []
right_publications = []
for pub in data_by_publication:
    if bias_ratings[pub] == 'left':
        left_publications.extend(data_by_publication[pub])

    if bias_ratings[pub] == 'right':
        right_publications.extend(data_by_publication[pub])

print('Total of ' + str(len(right_publications)) + ' right articles!')
print('Total of ' + str(len(left_publications)) + ' left articles!')
