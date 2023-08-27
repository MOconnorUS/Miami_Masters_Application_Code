#### Miami 4 + 1 Masters Application Object Oriented Project
#### Matthew O'Connor

# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from dateutil.parser import parse
import selenium
import requests
import re
import datetime
import time
import math

### Information being extracted ###
# Date and Time 
# Tournament Title 
# Entry Fee 
# Platforms 
# Regions 
# Skill 
# Requirements 
# Game 
# URL 

# @paths a list of URLs
# Removes all duplicates
# @return a list of unique URLs
def clean_links(paths):
    dupes = []
    unique = []

    for link in paths:
        if link in unique:
            dupes.append(link)
        else:
            unique.append(link)

    return unique

# @driver a selenium webdriver
# @url_begin the initial tournament page URL
# automatically navigates through all tournament pages to extract all URLs
# @return a list of urls
def get_link(driver, URL_begin):
    driver.get(URL_begin)

    num_tourneys_res = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pagination-count')))
    num_tourneys_list = num_tourneys_res.text.split(' ')
    num_tourneys = num_tourneys_list[4]
    max_iterations = int(num_tourneys) / 10
    max_iterations = math.floor(max_iterations)
    iterations = 0

    paths = []
    popup_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "mdl-button.mdl-js-button.css-ripple-effect.dark-button-secondary.button-small.css-ripple-activated")))
    popup_button.click()

    while True:
        try:
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.material-icons[mi-name='chevron_right']")))

            view_tournament_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'View Tournament')]")))
            tournament_links = [button.get_attribute('href') for button in view_tournament_buttons]
            

            for link in tournament_links:
                paths.append(link)

            
            iterations += 1
            next_button.click()

            if iterations > max_iterations:
                break

        except TimeoutException:
            break
        except StaleElementReferenceException:
            break
        except ElementClickInterceptedException:
            break

    paths = clean_links(paths)

    return paths

# CMG Tournament Object
class CMG_Tourney:
    # Default constructor initializing all parameters of the Object
    def __init__(self):
        self.date = None
        self.time = None
        self.title = None
        self.entry = None
        self.region = None
        self.platforms = None
        self.game = None
        self.requirements = None
        self.skill = None
        self.url = None

    # @soup a beautifulsoup4 element
    # extracts the date and time from an individual tournament page
    # @return a list containing the date and time of the specific tournament page
    def __datetime(soup):
        date_time_res = soup.find_all('span', {'class': 'tournament-details-date-text'})
        date_time_abrev = date_time_res[0].text.strip()
        abrev_month = parse(date_time_abrev[0:date_time_abrev.find(' ')])
        month = abrev_month.strftime('%B')
        date_time_abrev = date_time_abrev[date_time_abrev.find(' '):]

        date_time = month + date_time_abrev
        date_time_list = date_time.split()

        fin_time = date_time_list[2] + ' ' + date_time_list[3]
        day = date_time_list[1][:-2]
        date = date_time_list[0] + ' ' + day + ', ' + abrev_month.strftime('%Y')

        fin_datetime = []
        fin_datetime.append(date)
        fin_datetime.append(fin_time)

        return fin_datetime

    # @soup a beautifulsoup4 element
    # extracts the title and platforms from an inidivual tournament page
    # @return a list containing the title and platforms of the specific tournament page 
    def __title_plat(soup):
        title_res = soup.find('h4')
        title_strip = title_res.text.strip()
        title_strip_upper = title_strip.upper()
        platforms = 'ALL'

        if title_strip_upper.find('FREE ENTRY') != -1:
            title_strip_upper = title_strip_upper[title_strip_upper.find('FREE ENTRY') + 11:]

        if title_strip_upper.find('NOV AM') != -1:
            title_strip_upper = title_strip_upper[title_strip_upper.find('NOV AM') + 7:]

        if title_strip_upper.find('NOVICE AMATEUR') != -1:
            title_strip_upper = title_strip_upper[title_strip_upper.find('NOVICE AMATEUR') + 15:]

        if title_strip_upper.find('AMATEUR EXPERT') != -1:
            title_strip_upper = title_strip_upper[title_strip_upper.find('AMATEUR EXPERT') + 15:]

        if title_strip_upper.find('CONSOLE ONLY') != -1:
            platforms = 'CONSOLE ONLY'
            title_strip_upper = title_strip_upper[title_strip_upper.find('CONSOLE ONLY') + 13:]
    
        title_plat = []
        title_plat.append(title_strip_upper)
        title_plat.append(platforms)

        return title_plat

    # @soup a beautifulsoup4 element
    # extracts the skill from an individual tournament page
    # @return the skill present on the specific tournament page
    def __skill(soup):
        skill_res = soup.find_all('span', {'class': 'elo-skill-level'})
        skill = []
        for i in skill_res:
            skill.append(i.text.strip())

        return skill

    # @soup a beautifulsoup4 element
    # extracts the region from an individual tournament page
    # @return the region present on the specific tournament page
    def __region(soup):
        region_res = soup.find('span', {'class': 'region-transparent-container'})
        region = region_res.text.strip()
    
        return region

    # @soup a beautifulsoup4 element
    # extracts the entry from an individual tournament page
    # @return the region present on the specific tournament page
    def __entry(soup):
        entry_res = soup.find('div', {'class': 'tournament-details-entry-info'})
        entry_str = entry_res.text.strip()
        entry_long = entry_str[entry_str.find('\n') + 1:]
        entry = entry_long[0:entry_long.find('\n')]
        
        return entry

    # @soup a beautifulsoup4 element
    # extracts the requirements from an individual tournament page
    # @return the requirements on the specific tournament page 
    def __req(soup):
        req_res = soup.find('span', {'class': 'tournament-details-ruleset-text'})
        if req_res == None:
            req = 'NONE'
            return req
        else:
            req_str = req_res.text.strip()
            req_str = req_str.upper()
            req = req_str[req_str.find('CONSOLE ONLY'):]

            return req

    # @soup a beautifulsoup4 element
    # extracts the game from an individual tournament page
    # @return the game on the specific tournament page
    def __game(soup):
        game_res = soup.find('div', {'class': 'tournament-details-info-header'})
        game_str = game_res.text.strip()
        game_str = game_str.upper()
        game = game_str[game_str.find('CALL'):game_str.find('II') + 2]

        return game

    # @driver a selenium webdriver
    # @url the url of a specific tournament
    # All methods are called and all parameters of the Object are now filled
    # @return a dictionary containing all the information extracted from a specific tournament
    def cmg_tourney_info(self, driver, URL):
        driver.get(URL)

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        date_time = self.__datetime(soup)
        dates = date_time[0]
        ttime = date_time[1]

        self.date = dates
        self.time = ttime

        title_platforms = self.__title_plat(soup)
        title = title_platforms[0]
        platforms = title_platforms[1]

        self.title = title
        self.platforms = platforms

        skill_list = self.__skill(soup)
        skills = ''
        if len(skill_list) == 0:
            skills = 'All'
        else:
            for i in skill_list:
                skills = i + ' ' + skills
    
        regions = self.__region(soup)
        entryfee = self.__entry(soup)
        req = self.__req(soup)
        games = self.__game(soup)

        self.region = regions
        self.entry = entryfee
        self.requirements = req
        self.game = games
        self.url = URL
    
        info = {"date": dates, "time": ttime, "title": title, "entry": entryfee, "region": regions, "platforms": platforms, "game": games, "requirements": req, "skill": skills}
        return info

    # @return the date stored within the object
    def get_date(self):
        return self.date
    
    # @return the time stored within the object
    def get_time(self):
        return self.time

    # @return the title stored within the object
    def get_title(self):
        return self.title

    # @return the entry stored within the object
    def get_entry(self):
        return self.entry

    # @return the region stored within the object
    def get_region(self):
        return self.region

    # @return the platforms stored within the object
    def get_platforms(self):
        return self.platforms

    # @return the game stored within the object
    def get_game(self):
        return self.game

    # @return the requirements stored within the object
    def get_requirements(self):
        return self.requirements

    # @return the skill stored within the object
    def get_skill(self):
        return self.skill

    # @return the url stored within the object
    def get_url(self):
        return self.url
