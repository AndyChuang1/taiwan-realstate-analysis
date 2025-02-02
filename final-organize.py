import os
import pandas as pd
import json
import numpy as np
from datetime import datetime
import argparse

# 定義基礎目錄路徑
basePath = os.path.dirname(os.path.abspath(__file__))
current_year = datetime.now().year
parks_df = pd.read_csv('taipei-park-count.csv')
gas_df = pd.read_csv('taipei-gas-station-count.csv')

# 定義一個函數來匹配公園數量
def get_park_count(community, parks_df):
    park_count = 0
    for idx, row in parks_df.iterrows():
        park_names = row["里"].split(',')
        if any(park_name in community for park_name in park_names):
            park_count += row["公園數量"]
    return park_count

def get_gas_station_count(community, gas_df):
    gas_station_count = 0
    for idx, row in gas_df.iterrows():
        li_names = row["里"].split(',')
        if any(li_name in community for li_name in li_names):
            gas_station_count += row["gas_station_count"]
    return gas_station_count

def get_absolute_path(relative_path):
    return os.path.abspath(os.path.join(basePath, relative_path))

def toHouseAge(row):
    try:
        if pd.isna(row): 
            return 'NA'
        yearInt = int(row)
        year = int(str(yearInt)[:-4]) + 1911
        house_age = current_year - year
        return house_age
    except Exception as e:
        print(f'Error in toHouseAge: {e}, row: {row}')
        return 'NA'

def toList(row):
    if row == 'no location': 
        return []
    fixed_string_data = row.replace("'", '"')
    list_data = json.loads(fixed_string_data)
    return np.array(list_data)

def findClosest(row):
    if len(row) == 0: 
        return 'NA'

    distances = [entry['distance_meter'] for entry in row]
    return min(distances)

def main():
    # 使用 argparse 接收參數
    parser = argparse.ArgumentParser(description="Process housing data.")
    parser.add_argument(
        '-c', '--city', help="城市名稱，例如：'臺北市', '新北市'", default='臺北市')
    parser.add_argument(
        '-y', '--year', help='資料年份,例如:112', type=int, default=112)

    args = parser.parse_args()

    # 動態組合檔案名稱
    fileName = f"{args.city}-{args.year}-{args.year}-merged"
    finalStr = '-final.csv'

    # 讀取檔案
    inputFilePath = get_absolute_path(f"{fileName}.csv")
    df = pd.read_csv(inputFilePath)

    # 資料處理
    df['MRTS'] = df['MRTS'].apply(toList)
    df['mrt_count'] = df['MRTS'].apply(len)
    df['closest_mrt_meters'] = df['MRTS'].apply(findClosest)
    df['house_age'] = df['建築完成年月'].apply(toHouseAge)
    df['里'] = df['里'].str.split(';').str[-1]
    # 確保 house_age 和 closest_mrt_meters 是數值型
    df['house_age'] = pd.to_numeric(df['house_age'], errors='coerce')
    df['closest_mrt_meters'] = pd.to_numeric(df['closest_mrt_meters'], errors='coerce')
    df_filtered = df[['單價元坪', '里', 'mrt_count', 'house_age','建物移轉總面積平方公尺','closest_mrt_meters']]

    # # 使用 groupby 並計算平均值，跳過 NA
    group_df = df_filtered.groupby('里', as_index=False).mean(numeric_only=True)

    # # 將欄位 A 和 B 都四捨五入到整數
    group_df[['mrt_count', 'house_age','closest_mrt_meters']] = df_filtered[['mrt_count', 'house_age','closest_mrt_meters']].applymap(lambda x: int(round(x)) if pd.notna(x) else x)

    # 新增 park_count 欄位
    group_df["park_count"] = group_df["里"].apply(lambda x: get_park_count(x, parks_df))

    group_df = pd.merge(group_df, gas_df, on="里", how="left")
    group_df["gas_station_count"] = group_df["gas_station_count"].fillna(0)
    group_df[['mrt_count', 'house_age','closest_mrt_meters']] = group_df[['mrt_count', 'house_age','closest_mrt_meters']].applymap(lambda x: int(round(x)) if pd.notna(x) else x)

    # # # 儲存結果
    outputFilePath = get_absolute_path(f"{fileName}{finalStr}")
    group_df.to_csv(outputFilePath, index=False)
    print(f"處理完成，結果已儲存至：{outputFilePath}")

if __name__ == "__main__":
    main()
