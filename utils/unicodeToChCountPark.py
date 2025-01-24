import csv
import json
from typing import Counter


# 讀取 JSON 檔案
input_file = '臺北市公園基本資料.json'  # 你的輸入檔案名
output_file = '臺北市公園基本資料output.json'  # 你想要儲存的輸出檔案名

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)  # 將 JSON 內容讀取並轉換為 Python 對象


# Count occurrences of each "pm_libie"
libie_count = Counter(item["pm_libie"] for item in data)

csv_file_path= 'park_count.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["里", "公園數量"])
    
    # Use Counter to count and directly write the CSV
    writer.writerows(libie_count.items())
# 在這裡可以對數據進行處理，例如轉換Unicode為中文（如果需要的話）

# 儲存處理後的 JSON 到新的檔案
# with open(output_file, 'w', encoding='utf-8') as file:
#     json.dump(data, file, ensure_ascii=False, indent=4)  # 確保能夠正確處理中文

# print(f"已將處理後的數據儲存到 {output_file}")