import pandas as pd

gas_station_df = pd.read_csv('Address_台北市加油站.csv')

# 擷取Response_Address裡的"里"資訊，並建立新欄位
gas_station_df['里'] = gas_station_df['Response_Address'].str.extract(r'(\w+里)')

# 統計每個"里"出現的次數
count_df = gas_station_df['里'].value_counts().reset_index()
count_df.columns = ['里', 'gas_station_count']

# 存成csv
output_path = "gas_station_count.csv"
count_df.to_csv(output_path, index=False)

