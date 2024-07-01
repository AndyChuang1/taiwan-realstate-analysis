
import os
import pandas as pd
import argparse
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

parser = argparse.ArgumentParser(
    description='Choose the location you want to analyze')
parser.add_argument(
    '-c', '--city', help="['臺北市','苗栗縣','花蓮縣','臺中市','臺中縣','臺東縣','基隆市','南投縣','澎湖縣','臺南市','彰化縣','陽明山','高雄市','雲林縣','金門縣','新北市','嘉義縣','連江縣','宜蘭縣','臺南縣','嘉義市','桃園縣','高雄縣','新竹市','新竹縣','屏東縣']", default='臺北市')
parser.add_argument(
    '-f', '--yearsfrom', help='from year, example"110', type=int, default=112)
parser.add_argument(
    '-t', '--yearsto', help='to year, example:111', type=int, default=112)
args = parser.parse_args()
location = args.city
fromYear = args.yearsfrom
toYear = args.yearsto


# 設定基準路徑為專案的根目錄
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 結合基準路徑和相對路徑來獲取絕對路徑


def get_absolute_path(relative_path):
    return os.path.abspath(os.path.join(basePath, relative_path))


# 讀取 MRT CSV 文件
address_df = pd.read_csv(get_absolute_path('init-data/address-sample.csv'))
organize_df = pd.read_csv(location+'-'+str(fromYear)+'-'+str(toYear)+'-'+'organize.csv')


if '土地位置建物門牌' in organize_df.columns:
    # 將 csvB 中的 '土地位置建物門牌' 欄位的值插入到 address_df 的 'Address' 欄位
    address_df['Address'] = organize_df['土地位置建物門牌'].values

address_df['id'] = range(1, len(address_df) + 1)
chunk_size = 10000
if len(address_df)>10000:
    # 計算需要多少個 CSV 檔案
    num_chunks = (len(address_df) // chunk_size) + 1 

    for i in range(num_chunks):
        # 切分 DataFrame 並存入 CSV
        chunk = address_df.iloc[i * chunk_size: (i + 1) * chunk_size]
        chunk.to_csv(location+str(fromYear)+'-'+str(toYear)+'_'+'address.csv', index=False)
