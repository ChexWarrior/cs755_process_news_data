import pandas as pd

def get_csv_data(file_path):
    return pd.read_csv(file_path, usecols=['title', 'publication'])

new_sources = set()
data_paths = [
    './articles1.csv',
    './articles2.csv',
    './articles3.csv',
]

# CSV Data as data frame
for path in data_paths:
    data = get_csv_data(path)

    for row in data.iterrows():
        new_sources.add(row[1]['publication'])

for publication in new_sources:
        print(publication)

