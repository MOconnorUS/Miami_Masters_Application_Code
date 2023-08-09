#### uSync LLC
#### Matthew O'Connor, Co-Founder

# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from dateutil.parser import parse
from dateutil.parser import parser
from datetime import datetime, timedelta
import selenium
import requests
import re
import datetime
import time
import calendar

# Info
# Date and Time - done
# Tournament Title - done 
# Entry Fee - done
# Platforms - done
# Regions - done
# Skill - done
# Requirements - done
# Game - done
# URL - done

# URL_begin = "https://gamebattles.majorleaguegaming.com/tournaments"
# URL = "https://gamebattles.majorleaguegaming.com/x-play/call-of-duty-modern-warfare-ii/tournament/MWII17970/info"
# driver = webdriver.Chrome(ChromeDriverManager().install())
# time = '4:05 PM'

# Gets all URLs
def get_link(soup, good_nums):
    href_res = soup.find('a', {'class': 'image-wrapper'})
    href = href_res.get('href')
    href_num = href[href.find('MWII') + 4:]
    href_num_list = []
    href_list = []
    tempHref = href[:href.find('MWII') + 4]
    href_num = int(href_num)

    if good_nums[0] == 0:
        good_nums = good_nums[1:]
    # for num in good_nums:
    #     href_num_list.append(href_num + num)
    i = 0
    for num in good_nums:
        href_num_list.append(href_num + i)
        i += 1
    
    # href_list.append(href + '/info')
    for nums in href_num_list:
        href_list.append(tempHref + str(nums) + '/info')

    return href_list

# turns month abbreviation to full month
def convert_abbreviation(tempMonth):
    try:
        month = list(calendar.month_abbr).index(tempMonth)
        full_month = calendar.month_name[month]
        return full_month
    except ValueError:
        return None

# Gets platforms for tournament
# Gets prize for tournament
def get_info(driver, URL):
    driver.get(URL)
    tes = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'h3')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    datetime_res = soup.find_all('b', {'_ngcontent-serverapp-c306': True})
    # print(datetime_res)
    datetime_list = datetime_res[1].text.strip().split(' ')
    datetime_list[2] = convert_abbreviation(datetime_list[2])
    date = datetime_list[2] + ' ' + datetime_list[1] + ', ' + datetime_list[3]
    date = date[:len(date) - 1]

    time = datetime_list[4] + ' ' + datetime_list[5]

    req = 'NONE'
    title_res = soup.find('h3')
    title_list = title_res.text.strip()
    split_list = title_list.split('|')

    if split_list[2].find('Only') != -1:
        req = split_list[2][:split_list[2].find('Only') + 4]
        split_list[2] = split_list[2][split_list[2].find('Only') + 4:len(split_list[2]) - 1]

    if split_list[2].find('Only') != -1:
        req = req + ' ' + split_list[2][:split_list[2].find('Only') + 4]
        split_list[2] = split_list[2][split_list[2].find('Only'):len(split_list[2]) - 1]

    
    split_list[3] = req
    fin_list = split_list

    info_res = soup.find_all('div', {'class': 'detail-row'})
    entry_list = info_res[0].text.strip()
    entry = entry_list.split('\n')
    entry = entry[len(entry) - 1]
    info_list = []

    flag = 0
    for i in info_res:
        if flag != 0:
            info_list.append(i.text.strip())
        flag += 1
    
    platforms_res = info_list[1]
    platforms_list = platforms_res.split('\n')
    fin_platforms_list = []

    for j in platforms_list:
        if j == 'platforms' or j == '':
            dummy = j
        else:
            fin_platforms_list.append(j)
    
    platforms = ''
    if len(fin_platforms_list) == 3:
        platforms = 'All'
    elif len(fin_platforms_list) == 2:
        platforms = 'Console Only'
    else:
        if fin_platforms_list[0] == 'Xbox':
            platforms = 'Xbox'
        else:
            platforms = 'Playstation'

    prize_res = info_list[len(info_list) - 1]
    prize = prize_res[prize_res.find('e') + 1:prize_res.find('U') - 1]

    plat_prize_entry_skill_game = []
    skill = "All"
    game = "Modern Warfare II"
    plat_prize_entry_skill_game.append(entry)
    plat_prize_entry_skill_game.append(platforms)
    plat_prize_entry_skill_game.append(prize)
    plat_prize_entry_skill_game.append(skill)
    plat_prize_entry_skill_game.append(game)

    info = {"date": date, "time": time, "title": fin_list[2], "entry": entry, "region": fin_list[0], "platforms": platforms, "game": game, "requirements": fin_list[3], "skill": skill}
    return info

# Gets correct year correlated with time
def get_correct_year(time):
    current_datetime = datetime.datetime.now()
    current_year = current_datetime.strftime('%Y')

    if time.find(':') != 2:
        time = '0' + time

    time_format = '%I:%M %p'
    given_time = datetime.datetime.strptime(time, time_format)

    given_datetime = current_datetime.replace(
        hour=given_time.hour,
        minute=given_time.minute,
        second=0,
        microsecond=0
    )

    if given_datetime < current_datetime:
        given_datetime += timedelta(days=1)
    
    if given_datetime.year > int(current_year):
        future_year = given_datetime.year
    else:
        future_year = current_year
    
    return future_year

# Clicks on more info button
def extend_page(driver, URL):
    driver.get(URL)

    while True:
        try:
            more_info = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[gb-button]')))
            more_info.click()
        # except TimeoutException:
        #     break
        except StaleElementReferenceException:
            break
        except ElementClickInterceptedException:
            continue 
    
    date_link_list = get_count_datetime_img(driver, URL)

    return date_link_list

# Accesses all game images to differentiate CoD from other games
# Accesses countdown timer to see how long tournament starts in
# Gets date and time of each tournament
# returns list of all dates and times
def get_count_datetime_img(driver, URL):
    # Find all gb-tournament-card elements
    cards = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'gb-tournament-card.ng-star-inserted')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    game_img = soup.find_all('img', {'_ngcontent-serverapp-c363': True})

    game_img_list = []
    for j in game_img:
        game_img_list.append(j.get('src'))

    bad_nums = []
    good_nums = []
    for index, link in enumerate(game_img_list):
        if link.find('5eefd920-ed2d-489c-855d-b542548a36df-300x400?v=1664387167') == -1:
            bad_nums.append(index)
        else:
            good_nums.append(index)

    # Iterate through each gb-tournament-card
    for index, card in enumerate(cards):
        if index not in bad_nums:
            # Find the gb-countdown element within the card
            countdown = card.find_element(By.CSS_SELECTOR, "gb-countdown")

            # Extract the time from the element
            # Figure out what if anything I want to do with the countdown timer
            time = countdown.text

    datetime_res = soup.find_all('div', {'style': 'margin-bottom: 4px; flex-direction: row; box-sizing: border-box; display: flex; place-content: center flex-start; align-items: center;'})
    datetime_list = []

    bad_nums.sort(reverse=True)
    date = ''
    time = ''
    
    for i in datetime_res:
        temp = i.text.strip().split(' ')
        time = temp[5] + ' ' + temp[6]
        tempMonth = temp[2]
        month = convert_abbreviation(tempMonth)

        date = month + ' ' + temp[3] + ', ' + get_correct_year(time)

        datetime_list.append(date)
        datetime_list.append(time)
    
    for index in bad_nums:
        datetime_list.pop(index * 2)
        datetime_list.pop(index * 2)

    # print(datetime_list)
    # print(good_nums)
    # print(bad_nums)

    link_tes = soup.select('gb-tournament-card')
    for link in link_tes:
        links = link.select('a')
        print(links)
        for tes in links:
            href = tes['href']
            print(href)
    # print(link_tes)

    # link_list = get_link(soup, good_nums)

    # print(link_list)

    date_link_list = []
    # print(len(link_list))
    # print(len(datetime_list))

    # while len(link_list) > 0:
    #     temp = {"date": datetime_list[0], "time": datetime_list[1], "url": link_list[0]}
    #     datetime_list = datetime_list[2:]
    #     link_list = link_list[1:]
    #     date_link_list.append(temp)
    return date_link_list

# def main(driver, URL):
# get_link(driver, URL_begin)
# get_region_size_title_date_req(driver, URL)
# print(get_info(driver, URL))
# get_count_datetime_img(driver, URL_begin)
# get_correct_year(time)
# tes = extend_page(driver, URL_begin)
# print(tes[0]['date'])
# get_main_list(driver, URL_begin, URL)
# print(get_info(driver, URL))
