import pandas as pd
import argparse

parser = argparse.ArgumentParser(
    description='Choose the location you want to analyze')

parser.add_argument(
    '-m', '--merge', help='Its merge action', type=bool, default=False)
parser.add_argument(
    '-f', '--filename', help='台北市102-102_updated_address.csv', type=str, default='台北市102-102_updated_address.csv')
args = parser.parse_args()
isMerge = args.merge
fileName = args.filename




part1='p1'
part2='p2'

if not isMerge:
    # 讀取 CSV 檔案
    csv = pd.read_csv(fileName)
    # 按照索引分割
    split_index = int(len(csv) * 0.5)
    p1 = csv.iloc[:split_index] 
    p2 = csv.iloc[split_index:]

    # 將分割後的資料存回 CSV
    p1.to_csv(f'{part1}-{fileName}', index=False)
    p2.to_csv(f'{part2}-{fileName}', index=False)
else:

    # 讀取 CSV 檔案
    csv1 = pd.read_csv(f'{part1}-{fileName}')
    csv2 = pd.read_csv(f'{part2}-{fileName}')

    merged_data = pd.concat([csv1, csv2], ignore_index=True)

    # 將合併後的資料存回 CSV
    merged_data.to_csv('merged_data102.csv', index=False)
