#### Miami 4 + 1 Masters Application Object Oriented Project
#### Matthew O'Connor

# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import re
import os
import shutil
from pymongo_get_database import get_database

# @data a list of tournament objects
# Date, time, title, entry, region, platforms, game, requirements, and skill are extracted from a tournament
# The information builds a json object that is then inserted into a mongo db database
# @return None
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

# @data a list of tournament objects
# Date, time, and url are extracted from a tournament
# The information builds a json object that is then inserted into a mongo db database
# @return None
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
