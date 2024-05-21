import requests
import os
import zipfile
import time
import argparse


# 解析指令 
parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument(
    '-f', '--yearsfrom', help='from year, example"110', type=int, default=111)
parser.add_argument(
    '-t', '--yearsto', help='to year, example:111', type=int, default=112)
args = parser.parse_args()


def real_estate_crawler(year, season):
    if year > 1000:
        year -= 1911

    # download real estate zip file
    res = requests.get("https://plvr.land.moi.gov.tw//DownloadSeason?season=" +
                       str(year)+"S"+str(season)+"&type=zip&fileName=lvr_landcsv.zip")

    # save content to file
    fname = str(year)+str(season)+'.zip'
    open(fname, 'wb').write(res.content)

    fileFolder = 'real_estate/'
    if not os.path.isdir(fileFolder):
        os.mkdir(fileFolder)

    # make additional folder for files to extract
    folder = fileFolder + str(year) + '-s'+str(season)
    if not os.path.isdir(folder):
        os.mkdir(folder)

    # extract files to the folder
    with zipfile.ZipFile(fname, 'r') as zip_ref:
        zip_ref.extractall(folder)

    time.sleep(1)


fromYear = args.yearsfrom
toYear = args.yearsto


for year in range(fromYear, toYear+1):
    for season in range(1, 5):
        print(year, season)
        real_estate_crawler(year, season)
