import pandas as pd

def get_csv_data(file_path):
    frame = pd.read_csv(file_path, usecols=['title', 'publication'])

    return frame

new_sources = set()
data_paths = [
    './articles1.csv',
    './articles2csv',
    './articles3.csv',
]

# CSV Data as data frame
data = get_csv_data('./articles1.csv')

for row in data.iterrows():
    # print(row[1]['publication'])
    new_sources.add(row[1]['publication'])

for publication in new_sources:
    print(publication)

