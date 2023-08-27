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
            "date": i.get_date(),
            "time": i.get_time(),
            "title": i.get_title(),
            "entry": i.get_entry(),
            "region": i.get_region(),
            "platforms": i.get_platforms(),
            "game": i.get_game(),
            "requirements": i.get_requirements(),
            "skill": i.get_skill()
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
            "date": i.get_date(),
            "time": i.get_time(),
            "url": i.get_url()
        }        

        collection_name.insert_one(link_num)
        num += 1

    return None
