import os
import re
import pandas as pd
import geohash

# 設定基準路徑為專案的根目錄
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 結合基準路徑和相對路徑來獲取絕對路徑


def get_absolute_path(relative_path):
    return os.path.abspath(os.path.join(basePath, relative_path))


def extract_ri(address):
    match = re.search(r'(.+里)', address)
    if match:
        return match.group(1)
    else:
        return None


# 讀取 MRT CSV 文件
mrt_df = pd.read_csv(get_absolute_path('init-data/geohash-northern-mrt.csv'))


def findCloseMRT(row):
    print(row['緯度'], row['經度'])
    curGeoHash = geohash.encode(row['緯度'], row['經度'])
    for index, row in mrt_df.iterrows():
        precision6 = row['geohash'][0:7]  # W:1.2km , H:609.4m
        precision5 = row['geohash'][0:6]  # W:4.9km , H:4.9km

        if curGeoHash[0:7] == precision6:
            print(f"Index: {index}, Row: {row.to_dict()}")
        if curGeoHash[0:6] == precision5:
            print(f"Index: {index}, Row: {row.to_dict()}")

    return 1


initSourcePath = get_absolute_path('init-data')

address_df = pd.read_csv(initSourcePath+'/台北112_Address_Finish.csv')
address_df['里'] = address_df['Response_Address'].apply(extract_ri)


organize_df = pd.read_csv(basePath+'/台北市-112-112-merged.csv')
merged_df = pd.concat([organize_df, address_df['里'],
                      address_df['Response_X'], address_df['Response_Y']], axis=1)
merged_df.rename(columns={'Response_X': '經度',
                 'Response_Y': '緯度'}, inplace=True)


merged_df['MRTS'] = merged_df.apply(findCloseMRT, axis=1)

# merged_df.to_csv(basePath+'/台北市-112-112-merged.csv')


# TODO: 經緯度covert to geoHash
# TODO: For each row compare to 捷運 看哪個捷運站最近 在 轉換成距離
