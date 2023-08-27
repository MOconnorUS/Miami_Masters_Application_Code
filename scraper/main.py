#### Miami 4 + 1 Masters Application Object Oriented Project
#### Matthew O'Connor

# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import requests
import re
import time

# CMG
from cmg_scraper import get_link, CMG_Tourney

# Cod Agent
from eagent_scraper import EAGENT_Tourney, get_tournament_ids

from data_writer import write_all, write_all_links
from drop_info import drop_all_tourneys, drop_all_links

# @tournament_ids a list containing valid eagent tournament ids
# @url_begin the initial eagent tournament url
# @return a list of valid eagent tournament urls
def get_eagent_urls(tournament_ids, URL_begin):
    urls = []
    for i in range(len(tournament_ids)):
        url = URL_begin + "/tournament" + str(tournament_ids[i]['url'])
        urls.append(url)

    return urls

# @driver a selenium webdriver
# extracts all valid cmg tournament links and eagent tournament links
# @return a dictionary containing a list of cmg tournament links using the 'CMG' key and a list of eagent links using the 'EAGENT' key
def get_links(driver):
    CMG_URL = "https://www.checkmategaming.com/tournament/cross-platform/call-of-duty-modern-warfare-ii"
    
    cmg_links = get_link(driver, CMG_URL)

    URL_begin = "https://esportsagent.gg"

    tourney_ids = get_tournament_ids(driver, URL)
    eagent_urls = get_eagent_urls(tourney_ids, URL_begin)

    url_dict = {"CMG": cmg_links, "EAGENT": eagent_urls}
    return url_dict

# @driver a selenium webdriver
# @cmg_urls a list of valid cmg urls
# creates list of objects containing information from each url
# @return a list of cmg_tourney objects
def pop_cmg(driver, cmg_urls):
    cmg_tourneys = []

    for url in cmg_urls:
        cmg_tourney = CMG_Tourney
        cmg_tourney.cmg_tourney_info(driver, url)

        cmg_tourneys.append(cmg_tourney)

    return cmg_tourneys

# @driver a selenium webdriver
# @eagent_urls a list of valid eagent_urls
# creates a list of objects containing information from each url
# @return a list of eagent_tourney objects
def pop_eagent(driver, eagent_urls):
    eagent_tourneys = []

    for url in eagent_urls:
        eagent_tourney = EAGENT_Tourney
        eagent_tourney.get_tournament_info(driver, url)

        eagent_tourneys.append(eagent_tourney)

    return eagent_tourneys

# initially drops all tournaments and links from the database to ensure only new data is entered
# objects are then created and populated into the various documents within the database
# @return None
def main():
    drop_all_tourneys()
    drop_all_links()

    driver = webdriver.Chrome(ChromeDriverManager().install())

    link_list = get_links(driver)
    cmg_urls = link_list['CMG']
    eagent_urls = link_list['EAGENT']

    cmg_list = pop_cmg(driver, cmg_urls)
    eagent_list = pop_eagent(driver, eagent_urls)

    tourney_list = []
    url_list = []
    
    for tourney in cmg_list:
        tourney_list.append(tourney)

    for tourney in eagent_list:
        tourney_list.append(tourney)

    write_all(tourney_list)
    write_all_links(tourney_list)

    return None

main()