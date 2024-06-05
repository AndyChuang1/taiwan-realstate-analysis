import pandas as pd
import geohash
import os

# 設定基準路徑為專案的根目錄
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 結合基準路徑和相對路徑來獲取絕對路徑


def get_absolute_path(relative_path):
    return os.path.abspath(os.path.join(basePath, relative_path))


filePath = get_absolute_path('init-data/northern-mrt.csv')


# 讀取 CSV 文件
df = pd.read_csv(filePath)

# 定義一個函數將經緯度轉換為 geohash


def latlon_to_geohash(row):
    return geohash.encode(row['lat'], row['lon'])


# 應用函數到 DataFrame 的每一行，並新增一個 geohash 欄位
df['geohash'] = df.apply(latlon_to_geohash, axis=1)

# 將結果寫回到新的 CSV 文件
df.to_csv(basePath+'/geohash-northern-mrt.csv', index=False)
