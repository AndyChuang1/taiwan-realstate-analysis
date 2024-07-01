import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(
    description='Choose the location you want to analyze')

# parser.add_argument(
#     '-m', '--merge', help='Its merge action', type=bool, default=False)
# parser.add_argument(
#     '-f', '--filename', help='台北市102-102_updated_address.csv', type=str, default='台北市102-102_updated_address.csv')
parser.add_argument(
    '-c', '--city', help='臺北市', type=str, default='臺北市')
parser.add_argument(
    '-y', '--year', help='112', type=str, default='112')
args = parser.parse_args()
city = args.city
year = args.year




# part1='p1'
# part2='p2'

# if not isMerge:
#     # 讀取 CSV 檔案
#     csv = pd.read_csv(fileName)
#     # 按照索引分割
#     split_index = int(len(csv) * 0.5)
#     p1 = csv.iloc[:split_index] 
#     p2 = csv.iloc[split_index:]

#     # 將分割後的資料存回 CSV
#     p1.to_csv(f'{part1}-{fileName}', index=False)
#     p2.to_csv(f'{part2}-{fileName}', index=False)
# else:

#     # 讀取 CSV 檔案
#     csv1 = pd.read_csv(f'{part1}-{fileName}')
#     csv2 = pd.read_csv(f'{part2}-{fileName}')

#     merged_data = pd.concat([csv1, csv2], ignore_index=True)

#     # 將合併後的資料存回 CSV
#     merged_data.to_csv(f'{city}{year}_Address_finish.csv', index=False)

# 列出當前目錄下所有以 'p' 開頭且以 '_address.csv' 結尾的檔案
csv_files = [f for f in os.listdir('.') if f.startswith('p') and f'{city}' in f and f'{year}' in f and f.endswith('_address.csv')]

# 用來存放所有讀入的 DataFrame 的列表
dataframes = []

# 讀取每個 CSV 檔案並加入列表
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# 將所有 DataFrame 合併成一個
combined_df = pd.concat(dataframes, ignore_index=True)
combined_df.to_csv(f'{city}{year}_Address_finish.csv', index=False)