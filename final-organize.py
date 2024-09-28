

import os
import pandas as pd
import ast
import json
import numpy as np
from datetime import datetime


basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fileName = '臺北市-112-112-merged'
finalStr = '-final.csv'
current_year = datetime.now().year


def get_absolute_path(relative_path):
    return os.path.abspath(os.path.join(basePath, relative_path))

df = pd.read_csv(fileName+'.csv')

def toHouseAge(row):
    try:
        if pd.isna(row): return 'NA'
        yearInt = int(row)
        year = int(str(yearInt)[:-4])+1911
        house_age = current_year - year
        return house_age
    except Exception as e:
        print(f'Error in toHouseAge: {e}, row: {row}')
        return 'NA'

def toList(row):
    if row == 'no location': return []
    fixed_string_data = row.replace("'", '"')
    list_data = json.loads(fixed_string_data)
    return np.array(list_data)

def findClosest(row):
    if len(row) ==0: return 'NA'

    distances = [entry['distance_meter'] for entry in row]
    return min(distances)

# print(list(df['MRTS']))

df['MRTS'] = df['MRTS'].apply(toList)

df['mrt_count'] = df['MRTS'].apply(len)
df['closest_mrt_meters'] = df['MRTS'].apply(findClosest)
df['house_age'] = df['建築完成年月'].apply(toHouseAge)

df.to_csv(fileName+finalStr, index=False)
