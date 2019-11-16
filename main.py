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


# Deterine label of titles by source

# Drop any center sources

# Concatenate left and right sources

# Clean data?
