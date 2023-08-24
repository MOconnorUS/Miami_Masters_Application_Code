#### uSync LLC
#### Matthew O'Connor, Co-Founder

# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import re
import datetime
import dateutil
import time
from dateutil import tz
from dateutil.parser import parse
from datetime import datetime

# Test Data
# Codagent tournament page, testing valid tournaments
# URL = https://esportsagent.gg/tournament

# Info
# Date and Time
# Per Person/Entry
# Team Size
# Format
# Game
# Platform
# Link

# **Notes**
# Need to sift through titles to see if there is a '*' and if so move everything until the next '*' to requirements if it doesnt contain
# a skill requirement within it, need to look for one of the various skill levels and check if there is a no before it 
# if so then import "no skill" into skill else import "skill only" into skill
# Need to check to see what platforms it contains and then do either console only or NONE
# Filter game to only contain MW2

# URL = "https://esportsagent.gg/tournament/13162598"
# URL_begin = "https://esportsagent.gg/tournament"
# driver = webdriver.Chrome(ChromeDriverManager().install())

def get_dates(soup):
        datetimes_res = soup.find_all('div', {'class': 'text-gray-700 text-[13px] uppercase letter tracking-wide'})
    
        datetimes_list = []
        for i in datetimes_res:
            datetimes = i.text.strip().split(' ')

            date = datetimes[0] + ' ' + datetimes[1] + ' ' + datetimes[2]
            time = datetimes[3] + ' ' + datetimes[4]

            datetimes_list.append(date)
            datetimes_list.append(time)
    
        return datetimes_list

    # Inputs: driver, URL_begin
    # Returns: a list of all the valid tournament links for the day
    # Note: esportsagent.gg returns <Response [500]> if broken link and <Response [200]> if valid
    def get_tournament_ids(driver, URL_begin):
        init_id_list = []
        id_list = []
        driver.get(URL_begin)
        tes = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.grid.md\\:grid-cols-2.lg\\:grid-cols-3.gap-4')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    
        datetimes_list = get_dates(soup)

        live_tournaments = soup.find_all('div', {'class': 'grid md:grid-cols-2 lg:grid-cols-3 gap-4'})
        for c in live_tournaments[0].children:
            a = c.find('a')
            init_id_list.append(a.get('href'))

        while len(init_id_list) > 0:
            temp = {'date': datetimes_list[0], 'time': datetimes_list[1], 'url': init_id_list[0][11:]}
            datetimes_list = datetimes_list[2:]
            init_id_list = init_id_list[1:]

            id_list.append(temp)

        return id_list

    def get_tournament_link(id_list, URL):
        tournament_links = []
    
        for i in range(len(id_list)):
            tournament_links.append(URL + str(id_list[i]['url']))

        link_list = []
        for link in range(len(tournament_links)):
            temp = {'date': id_list[link]['date'], 'time': id_list[link]['time'], 'url': tournament_links[link]}
            link_list.append(temp)

        return link_list

class EAGENT_Tourney:
    def __init__(self, driver, url):
        tourney_info = get_tournament_info(driver, url)
        self.date = tourney_info['date']
        self.time = tourney_info['time']
        self.title = tourney_info['title']
        self.entry = tourney_info['entry']
        self.region = tourney_info['region']
        self.platforms = tourney_info['platforms']
        self.game = tourney_info['game']
        self.requirements = tourney_info['requirements']
        self.skill = tourney_info['skill']
        self.url = url

    def __conv_time(x):
        x_str = x.strftime("%Y-%m-%d %H:%M:%S")
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/New_York')
        utc = datetime.strptime(x_str, '%Y-%m-%d %H:%M:%S')
        utc = x.replace(tzinfo=from_zone)
        east = utc.astimezone(to_zone)
        hour = int(east.strftime('%I'))
        minute = int(east.strftime('%M'))
        date = east.strftime('%m-%d-%Y')
        # print(east)
        return east

    # Inputs: driver, tourney URL
    # Returns: all tournament information
    def get_tournament_info(driver, URL):
        driver.get(URL)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # live_tournaments = soup.find_all('div', {'class': 'grid md:grid-cols-2 lg:grid-cols-3 gap-4'})

        # Need this to compare to see if the game is MW2 or not
        # Game
        #span was 'text-white font-semibold'
        game_res = soup.find_all('span', {'class': 'uppercase text-[#8E8EA1] text-sm pr-3'})
        games = game_res[0].text.strip()
        game = ''
        info = {}
        if games == 'Modern Warfare II':
            game = games    

            # Date and time, look words but figure out if its needed or if i can loop through all available tournaments in the data writer
            # IMPORTANT: look at main in the esportsagent git hub under the ld3 branch and see what he does to create a list of dictionaries rather
            # than dictionary of lists
            # div tag is 'text-gray-500 uppercase text-sm font-roboto'
            date_time_res = soup.find_all('div', {'class': 'text-gray-500 uppercase text-sm font-roboto'})
            date_time = date_time_res[0].text.strip()
            date_time_list = date_time.split()
            date = date_time_list[0] + " " + date_time_list[1] + " " + date_time_list[2]
            # print(date)
            time = date_time_list[3]
            ampm = date_time_list[4]
            # print(time)
            # print(ampm)
            time_parsed = parse(time)
            # print(type(time_parsed))
            res = self.__conv_time(time_parsed)
            # print(res)
            mins = ""      
            # print(type(res.hour))
            new_time = ''
    
            # If the minute = 0 it will add another 0 otherwise it will only output 1 0 in result
            # If the hour is greater than 12 it is set to -12 to keep it on a 12 hour clock
            # If the hour is equal to 0 it is changed to 12 to keep it on a 12 hour clock
            # new_time is the string containing the hours and minutes in the form hours:minutes
            if (res.minute == 0):
                if (res.hour > 12):
                    hrs = res.hour - 12
                    mins = str(res.minute) + "0"
                    new_time = '{}:{}'.format(hrs, mins)
                elif (res.hour == 0):
                    hrs = 12
                    mins = str(res.minute) + "0"
                    new_time = '{}:{}'.format(hrs, mins)
                else:
                    mins = str(res.minute) + "0"
                    new_time = '{}:{}'.format(res.hour, mins)
            else:
                if (res.hour > 12):
                    hrs = res.hour - 12
                    new_time = '{}:{}'.format(hrs, mins)
                elif (res.hour == 0):
                    hrs = 12
                    mins = str(res.minute) + "0"
                    new_time = '{}:{}'.format(hrs, mins)
                else:
                    new_time = '{}:{}'.format(res.hour, res.minute)

    
            # If the hour is less than 12 but greater than or equal to 8 and it is AM it will change to PM and vice versa
            if ((res.hour - 12) < 12 and (res.hour - 12) >= 8):
                if (ampm == "AM"):
                    ampm = "PM"
            elif (res.hour < 12 and res.hour >= 8):
                if (ampm == "PM"):
                    ampm = "AM"
    
            new_time += " " + ampm

            # Tourney Title, Requirements from title, Skill from title
            # span for white text is 'font-semibold text-2xl lg:text-3x1 max-w-[420px] break-words text-white'
            # span for gold text is 'font-semibold text-2xl lg:text-3xl max-w-[420px] break-words text-gold'
            # Gold text is only when the title_res is less than 1
            title_res = soup.find_all('span', {'class': 'font-semibold text-2xl lg:text-3xl max-w-[420px] break-words text-white'})
            if len(title_res) < 1:
                title_res = soup.find_all('span', {'class': 'font-semibold text-2xl lg:text-3xl max-w-[420px] break-words text-gold'})
            title = title_res[0].text.strip()

            pos2 = 0
            counter = 0
            req = 'NONE'
            skill = 'All'

            if title.find('*') != -1:
                for char in title:
                        if (char == '*' and counter != title.find('*')):
                            pos2 = counter
                            break
        
                        counter += 1

                special = title[title.find('*') + 1:pos2]
            
                if special == 'DOLLAR ENTRY':
                    title = title[0:title.find('*')] + title[pos2 + 2:]
                elif special.find('AGENTS') != -1 or special.find('MASTERS') != -1 or special.find('CHALLENGERS') != -1 or special.find('AMATEURS') != -1 or special.find('NOVICE') != -1:
                    title = title[0:title.find('*')] + title[pos2 + 2:]
                    skill = special
                else:
                    title = title[0:title.find('*')] + title[pos2 + 2:]
                    req = special

            pos2 = 0
            counter = 0
        
            if title.find('*') != -1:
                for char in title:
                    if (char == '*'):
                        pos2 = counter
        
                    counter += 1

                special = title[title.find('*') + 1:pos2]

                if special == 'DOLLAR ENTRY':
                    title = title[0:title.find('*')] + title[pos2 + 2:]
                elif special.find('AGENTS') != -1 or special.find('MASTERS') != -1 or special.find('CHALLENGERS') != -1 or special.find('AMATEURS') != -1 or special.find('NOVICE') != -1:
                    title = title[0:title.find('*')] + title[pos2 + 2:]
                    skill = special
                else:
                    title = title[0:title.find('*')] + title[pos2 + 2:]
                    req = special
    
        
            # Entry/Per Person
            # span was 'font-semibold text-white'
            per_person_res = soup.find_all('span', {'class': 'font-semibold text-white'})
            per_person = per_person_res[0].text.strip()

            # Platforms
            # div is 'flex gap-1
            logo_res = soup.find('div', {'class': 'flex gap-1'}).find_all('img')
            platforms = []
            logo_list = []
            plat = ''
            flag = 0
            for i in logo_res:
                logo_list.append(str(i))
            for j in logo_list:
                if j.find('xbox') != -1:
                    platforms.append('xbox')
                if j.find('playstation') != -1:
                    platforms.append('playstation')
                if j.find('steam') != -1:
                    platforms.append('steam')
                if j.find('battle.net') != -1:
                    platforms.append('battle.net')
    
            if len(platforms) == 4:
                plat = 'All'
            elif len(platforms) == 2:
                for i in platforms:
                    if i == 'xbox':
                        flag += 1
                    if i == 'playstation':
                        flag += 1
                if flag == 2:
                    plat = 'Console Only'
                else:
                    plat = 'PC Only'
            else:
                plat = platforms[0]
    
            # Region
            # span is 'uppercase text-[#8E8EA1] text-sm px-3'
            region_res = soup.find_all('span', {'class': 'uppercase text-[#8E8EA1] text-sm px-3'})
            region = region_res[0].text.strip()

            info = {"date": date, "time": new_time, "title": title, "entry": per_person, "region": region, "platforms": plat, "game": game, "requirements": req, "skill": skill}
        return info

    def get_date():
        return self.date
    
    def get_time():
        return self.time

    def get_title():
        return self.title

    def get_entry():
        return self.entry

    def get_region():
        return self.region

    def get_platforms():
        return self.platforms

    def get_game():
        return self.game

    def get_requirements():
        return self.requirements

    def get_skill():
        return self.skill

    def get_url():
        return self.url

# tourney_test = get_tournament_info(driver, URL)
# print(tourney_test["date"])
# print(get_tournament_link(driver, URL_begin))
# print(get_tournament_info(driver, URL))
# print(get_tournament_ids(driver, URL_begin))
# print(get_date())

# testinfo = {}
# testinfo = get_tournament_info(driver, URL)
# if (get_tournament_info(driver, URL) == testinfo):
#     print("tournament info method works")
# get_tournament_info(driver, URL)

# testid = {}
# testid = get_tournament_ids(driver, URL)
# if (get_tournament_ids(driver, URL) == testid):
#     print("tournament id method works")

# testlinks = {}
# testlinks = get_tournament_link(driver, URL)
# if (get_tournament_link(driver, URL) == testlinks):
#     print("tournament link method works")

# testdate = {}
# testdate = get_date()
# if (get_date() == testdate):
#     print("date method works")

# print(get_dates(driver, URL_begin))

# link_list = get_tournament_ids(driver, URL_begin)
# print(link_list)
# print(get_tournament_link(link_list, URL_begin))
    


        
        
