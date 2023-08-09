#### uSync LLC
#### Matthew O'Connor, Co-Founder

# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from web_scraper import get_tournament_info, get_date, get_tournament_link
import requests
import re
import csv
import os
import shutil
from pymongo_get_database import get_database


# use while loop to check the date using the getDate function created in web_scraper

# Test data
# test_data = [{'date': 'September 12, 2022', 'time': '10:20 PM', 'title': '2v2 1ND MW SND', 'entry': '$4', 'size': '2', 'platforms': ['xbox', 'playstation', 'battle.net'], 'game': 'Call of Duty Modern Warfare 2'}, {'date': 'September 12, 2022', 'time': '9:20 PM', 'title': '3v3 1ND CW SND', 'entry': '$4', 'size': '3', 'platforms': ['xbox', 'playstation', 'battle.net'], 'game': 'Call of Duty Modern Warfare 2'}]

# URL = "https://esportsagent.gg/tournament"
# driver = webdriver.Chrome(ChromeDriverManager().install())

# all_info = get_tournament_info(driver, URL)
# print(all_info)
# try using main since i have a bit more time
# tourney_links = get_tournament_link(driver, URL)

# def current_tournaments(tourney_links, driver, URL):
#     all_tourneys = []
#     for i in range(len(tourney_links)):
#         all_tourneys.append(get_tournament_info(driver, URL))
#         print(all_tourneys)

#     return all_tourneys

# print(current_tournaments(driver, URL))

def write_all(data):
    dbname = get_database()
    collection_name = dbname["tournaments"]
    num = 0
    
    for i in data:
        tournament_num = {
            "_id": num,
            "date": i["date"],
            "time": i["time"],
            "title": i["title"],
            "entry": i["entry"],
            "region": i["region"],
            "platforms": i["platforms"],
            "game": i["game"],
            "requirements": i["requirements"],
            "skill": i["skill"]
        }

        collection_name.insert_one(tournament_num)
        num += 1
    
    return None

def write_all_links(data):
    dbname = get_database()
    collection_name = dbname["links"]
    num = 0

    for i in data:

        link_num = {
            "_id": num,
            "url": data[num]
        }        

        collection_name.insert_one(link_num)
        num += 1

    return None




# Write all data to CSV file
# Input: data to write, optional path but will default to tournaments_data.csv
# Returns: None
# def write_all(data, path = "tournaments_data.csv"):

#     # Header for CSV file
#     header = ['Date', 'Time', 'Title', 'Entry', 'Team Size', 'Platforms', 'Gamemode']
#     field_names = ["date", "time", "title", "entry", "size", "platforms", "gamemode"]

#     # Case: 'tournaments data' file does not exist
#     # if not(os.path.isfile(path)):
#     with open(path, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(header)
#         dict_writer = csv.DictWriter(f, fieldnames=field_names)
#         dict_writer.writerows(data)

#         print("Done. New file Created")
#         return None


    # Case: 'tournaments data' exists
    # else:
    #     with open(path, 'r') as fr:
    #         read_data = []
    #         reader = csv.reader(fr)

    #         for line in reader:
    #             if line[4] != 'Size':
    #                 line[4] = eval(line[4])
    #             read_data.append(line)

    #         # removing unneeded header info
    #         read _ data = read_data[1:len(read_data)]

    # OVERALL_WRITE = 0
    # WRITE_FLAG = 0
    # new_data = []
    # for d in data:
    #     d_vals = list(d.values())
    #     for rd in read_data:
    #         if rd == d_vals:
    #             WRITE_FLAG = 0
    #             break
    #         else:
    #             WRITE_FLAG = 1
    #     if WRITE_FLAG:
    #         new_data.append(d_vals)
    #         OVERALL_WRITE = 1
    #         WRITE_FLAG = 0
    # all_data = new_data
    # if OVERALL_WRITE:
    #     with open(path, 'w', newline = '') as fw:
    #         writer = csv.writer(fw)
    #         writer.writerow(header)
    #         for ad in all_data:
    #             writer.writerow(ad)
    #         print("Done. New data written.")
    #         return None
    # else:
    #     print("Done. No new data written.")
    # return None

# print(write_all(test_data, "tournaments_data.csv"))
            

            


