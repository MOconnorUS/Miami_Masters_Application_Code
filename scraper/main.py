#### uSync LLC
#### Matthew O'Connor, Co-Founder

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
from eagent_scraper import EAGENT_Tourney, get_tournament_link, get_tournament_ids

from data_writer import write_all, write_all_links
from drop_info import drop_all_tourneys, drop_all_links

def get_eagent_urls(tournament_ids, URL_begin):
    urls = []
    for i in range(len(tournament_ids)):
        url = URL_begin + "/tournament" + str(tournament_ids[i]['url'])
        urls.append(url)

    return urls

def get_links(driver):
    CMG_URL = "https://www.checkmategaming.com/tournament/cross-platform/call-of-duty-modern-warfare-ii"
    
    cmg_links = get_link(driver, CMG_URL)

    URL_begin = "https://esportsagent.gg"

    tourney_ids = get_tournament_ids(driver, URL)
    eagent_urls = get_eagent_urls(tourney_ids, URL_begin)

    url_dict = {"CMG": cmg_links, "EAGENT": eagent_urls}
    return url_dict

def pop_cmg(driver, cmg_urls):
    cmg_tourneys = []

    for url in cmg_urls:
        cmg_tourney = CMG_Tourney
        cmg_tourney.cmg_tourney_info(driver, url)

        cmg_tourneys.append(cmg_tourney)

    return cmg_tourneys

def pop_eagent(driver, eagent_urls):
    eagent_tourneys = []

    for url in eagent_urls:
        eagent_tourney = EAGENT_Tourney
        eagent_tourney.get_tournament_info(driver, url)

        eagent_tourneys.append(eagent_tourney)

    return eagent_tourneys

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