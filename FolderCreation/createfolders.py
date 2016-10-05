import pandas as pd
import os

d = pd.read_excel('data.xlsx')
print("Found {} names.".format(len(d)))

for index, row in d.iterrows():
    path = '{}/{}'.format(row['Class'], row['Name'])
    print("Creating '{}'...".format(path))
    os.makedirs(path, exist_ok=True)

print("Done.")