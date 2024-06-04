import os
import re
import pandas as pd

def extract_ri(address):
    match = re.search(r'(.+里)', address)
    if match:
        return match.group(1)
    else:
        return None

    
address_df = pd.read_csv('Address_Finish.csv')
address_df['里'] = address_df['Response_Address'].apply(extract_ri)



organize_df = pd.read_csv('../台北市-整理-112-112.csv')
merged_df = pd.concat([organize_df, address_df['里'], address_df['Response_X'], address_df['Response_Y']], axis=1)
merged_df.rename(columns={'Response_X': '經度', 'Response_Y': '緯度'}, inplace=True)
merged_df.to_csv('../台北市Merge.csv')

# TODO: 捷運座標 to geoHash
# TODO: 經緯度covert to geoHash
# TODO: For each row compare to 捷運 看哪個捷運站最近 在 轉換成距離
