
import os
import pandas as pd
import argparse
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

parser = argparse.ArgumentParser(
    description='Choose the location you want to analyze')
parser.add_argument(
    '-c', '--city', help="['臺北市','苗栗縣','花蓮縣','臺中市','臺中縣','臺東縣','基隆市','南投縣','澎湖縣','臺南市','彰化縣','陽明山','高雄市','雲林縣','金門縣','臺北縣','嘉義縣','連江縣','宜蘭縣','臺南縣','嘉義市','桃園縣','高雄縣','新竹市','新竹縣','屏東縣']", default='臺北市')
parser.add_argument(
    '-f', '--yearsfrom', help='from year, example"110', type=int, default=112)
parser.add_argument(
    '-t', '--yearsto', help='to year, example:111', type=int, default=112)
args = parser.parse_args()
location = args.city
fromYear = args.yearsfrom
toYear = args.yearsto

location_str = """臺北市 A 苗栗縣 K 花蓮縣 U
臺中市 B 臺中縣 L 臺東縣 V
基隆市 C 南投縣 M 澎湖縣 X
臺南市 D 彰化縣 N 陽明山 Y
高雄市 E 雲林縣 P 金門縣 W
新北市 F 嘉義縣 Q 連江縣 Z
宜蘭縣 G 臺南縣 R 嘉義市 I
桃園縣 H 高雄縣 S 新竹市 O
新竹縣 J 屏東縣 T"""

# 設定基準路徑為專案的根目錄
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 結合基準路徑和相對路徑來獲取絕對路徑


def get_absolute_path(relative_path):
    return os.path.abspath(os.path.join(basePath, relative_path))


# create a dictionary to convert location to letter
locToLetter = dict(
    zip(location_str.split()[::2], location_str.lower().split()[1::2]))

sourceDataPath = get_absolute_path('init-data/real_estate')+'/'

# 歷年資料夾
dirs = [d for d in os.listdir(sourceDataPath) if not d.startswith('.DS')
        if int(d[:3]) >= fromYear and int(d[:3]) <= toYear]
dfs = []
print(dirs)
for d in dirs:
    df = pd.read_csv(os.path.join(
        sourceDataPath+d, locToLetter[location] + '_lvr_land_a.csv'), index_col=False)
    df['Q'] = d[-1]
    dfs.append(df.iloc[1:])

df = pd.concat(dfs, sort=True)

def add_city(address):
    if not address.startswith('臺北市'):
        return location + address
    return address

# 應用函數到地址欄位
df['土地位置建物門牌'] = df['土地位置建物門牌'].apply(add_city)

# 新增交易年份
df['year'] = pd.to_numeric(df['交易年月日'].str[:-4], errors='coerce') + 1911

# 平方公尺換成坪
df['單價元平方公尺'] = df['單價元平方公尺'].astype(float)
df['單價元坪'] = df['單價元平方公尺'] * 3.30579

# 建物型態
df['建物型態2'] = df['建物型態'].str.split('(').str[0]

# # 刪除有備註之交易（多為親友交易、價格不正常之交易）
df = df[df['備註'].isnull()]

# 刪除車位土地的資料
df = df[~df['交易標的'].isin(['車位', '土地'])]

df.index = pd.to_datetime(df['year'].astype(
    str) + df['交易年月日'].str[-4:], errors='coerce')
df.sort_index(inplace=True)

# 取出'鄉鎮市區'欄位並將其移除
city_column = df.pop('鄉鎮市區')
# 插入'鄉鎮市區'欄位到DataFrame的最前面
df.insert(0, '鄉鎮市區', city_column)
df.head()
df.to_csv(f'{location}-{str(fromYear)}-{str(toYear)}-organize.csv')
