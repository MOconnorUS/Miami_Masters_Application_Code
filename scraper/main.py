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

# GB
from gb_scraper import extend_page, get_info

# CMG
from cmg_scraper import get_link, get_cmg

# Cod Agent
from web_scraper import get_tournament_info, get_tournament_link, get_date, get_tournament_ids

from data_writer import write_all, write_all_links
from drop_info import drop_all_tourneys, drop_all_links

def get_all_info(tournament_ids, driver, URL, URL_begin):
    eagent_info = []
    for i in range(len(tournament_ids)):
        url = URL_begin + "/tournament" + str(tournament_ids[i]['url'])
        eagent_info.append(get_tournament_info(driver, url))

    return eagent_info

def sort_info_dicts(info_list):
    # date_str = info_list['date']
    # time_str = info_list['time']

    # info_dt = datetime.strptime(f"{date_str} {time_str}", "%B %d, %Y %I:%M %p")
    sorted_list = sorted(info_list, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%B %d, %Y %I:%M %p"))
    return info_dt

def sort_link_dicts(link_list):
    date_str = link_list['date']
    time_str = link_list['time']

    link_dt = datetime.strptime(f"{date_str} {time_str}", "%B %d, %Y %I:%M %p")
    return link_dt

def main():
    # drop_all_tourneys()
    # drop_all_links()

    # GB WORKS
    GB_URL = "https://gamebattles.majorleaguegaming.com/tournaments"
    driver = webdriver.Chrome(ChromeDriverManager().install())

    init_gb_links = extend_page(driver, GB_URL)
    gb_links = []
    gb_info = []

    for link in init_gb_links:
        print(link)
        gb_links.append(link)
        # gb_info.append(get_info(driver, link['url']))
    

    # write_all(gb_info)
    # write_all_links(gb_links)

    # CMG TESTING - works in main, havent tested importing to database yet
    # CMG_URL = "https://www.checkmategaming.com/tournament/cross-platform/call-of-duty-modern-warfare-ii"
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # cmg_links = get_link(driver, CMG_URL)
    # cmg_info = []


    # for link in cmg_links:
    #     cmg_info.append(get_cmg(driver, link))

    # cmg_sort_links = []
    # for datetime in range(len(cmg_info)):
    #     temp = {'date': cmg_info[datetime]['date'], 'time': cmg_info[datetime]['time'], 'url': cmg_links[datetime]}
    #     cmg_sort_links.append(temp)

    # write_all(cmg_info)
    # write_all_links(cmg_sort_links)

    # # Codagent WORKS
    URL = "https://esportsagent.gg/tournament"
    URL_begin = "https://esportsagent.gg"

    tourney_ids = get_tournament_ids(driver, URL)
    eagent_info = get_all_info(tourney_ids, driver, URL, URL_begin)
    
    fin_eagent_info = []
    bad_indexes = []

    for index,i in enumerate(eagent_info):
        if i:
            fin_eagent_info.append(i)
        else:
            bad_indexes.append(index)
        
    eagent_links = get_tournament_link(tourney_ids, URL_begin)

    bad_indexes.sort(reverse=True)
    for index in bad_indexes:
        eagent_links.pop(index)

    # write_all(fin_eagent_info)
    # write_all_links(all_links)
    print(gb_info)
    # print(eagent_info)

    # all_info = []
    # for info in gb_info:
    #     all_info.append(info)
    # for info in eagent_info:
    #     all_info.append(info)
    
    # # all_info = sort_info_dicts(all_info)
    # print(all_info)

main()