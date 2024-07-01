# taiwan-real-estate-analysis

## Crawler the source

`python3.1 crawler/index.py --yearsfrom 102  --yearsto 112`

## Preparation

move real_estate to init-data

## Analyze the source sample code

`python3.1 analysis/index.py --yearsfrom 102 --yearsto 112 --city 臺北市`

"""臺北市 A 苗栗縣 K 花蓮縣 U
臺中市 B 臺中縣 L 臺東縣 V
基隆市 C 南投縣 M 澎湖縣 X
臺南市 D 彰化縣 N 陽明山 Y
高雄市 E 雲林縣 P 金門縣 W
新北市 F 嘉義縣 Q 連江縣 Z
宜蘭縣 G 臺南縣 R 嘉義市 I
桃園縣 H 高雄縣 S 新竹市 O
新竹縣 J 屏東縣 T"""

## For merge lat and lon, calculate near MRT distance

1. `python3.1 trim/index.py -f 110 -t 110  -c 臺北市`
2. `python3.1 trim/convert-to-tgos.py -f 110 -t 110  -c 臺北市`
    - If rows are greater than 10000, csv will be split into smaller by 10000 rows each file.
3.  Upload 臺北市110-110_updated_address to https://www.tgos.tw/tgos/Addr
    - TGOS only supports 10000 records per day
4.  把Tgos回傳的檔案放到 程式資料夾的 init-data 並重新命名 臺北市110_Address_Finish
    -  if response of TGOS is multi part, merge to one part is necessary. rename TGOS file to p1-臺北市111-111_address_finish, p2-新北市111-111_address_finish `python3.1 merge-address.py -c 臺北市 -y 111`
5. `python3.1 trim/merge.py -y 110 -c 臺北市` 合併TGOS經緯度跟抓出捷運站距離

