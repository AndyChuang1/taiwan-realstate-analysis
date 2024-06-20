import pandas as pd

fileName = '台北市102-102_updated_address.csv'



part1='p1'
part2='p2'

# 讀取 CSV 檔案
csv = pd.read_csv(fileName)
# 按照索引分割
split_index = int(len(csv) * 0.5)
p1 = csv.iloc[:split_index]
p2 = csv.iloc[split_index:]

# 將分割後的資料存回 CSV
p1.to_csv(f'{part1}-{fileName}', index=False)
p2.to_csv(f'{part2}-{fileName}', index=False)


# 讀取 CSV 檔案
csv1 = pd.read_csv(f'{part1}-{fileName}')
csv2 = pd.read_csv(f'{part2}-{fileName}')

merged_data = pd.concat([csv1, csv2], ignore_index=True)

# 將合併後的資料存回 CSV
merged_data.to_csv('merged_data102.csv', index=False)