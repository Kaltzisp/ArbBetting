import re
import time
from abc import abstractmethod
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from src.core.utils import log, TEAM_MAPPING
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebScraper():
    def __init__(self, driver, hidden):
        self.source = self.__class__.__name__
        self.category_list = ['Popular', 'Player Points']
        self.market_list = {'Popular': ['Head To Head', 'Pick Your Own Line', 'Pick Your Own Total'], 'Player Points': ['Player Points']}
        if driver is None:
            driver_options = webdriver.ChromeOptions()
            if hidden:
                driver_options.add_argument("--headless")
                log.info(f"{self.source}: Running WebScraper...")
            else:
                driver_options.add_argument("--window-size=400,800")
            driver_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            driver_options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
        driver.implicitly_wait(10)
        self.driver = driver

    @abstractmethod
    def scrape_data(self):
        pass

    def scroll_click(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("javascript:window.scrollBy(0, -350)")
        element.click()

    def click_leg(self, category, market, leg):
        # turns off all categories
        for active_category in self.driver.find_elements(By.CLASS_NAME, '_1uszh93 '):
            self.scroll_click(active_category)

        category_dict = {i.text: i for i in self.driver.find_elements(By.CLASS_NAME, '_p1oke7 ')}
        self.scroll_click(category_dict[category])
        self.scroll_click(self.driver.find_element(By.CLASS_NAME, '_107y7tp '))
        market_dict = {i.text: i for i in self.driver.find_elements(By.CLASS_NAME, '_107y7tp ')}
        self.scroll_click(market_dict[market])
        button_dict = {i.text: i for i in self.driver.find_elements(By.CLASS_NAME, '_1k5b7ys ') + self.driver.find_elements(By.CLASS_NAME, '_ydwnsr ')}
        self.scroll_click(button_dict[leg])

    def switch_line(self, line):
        if line[0] == '+':
            return f'-{line[1:]}'
        return f'+{line[1:]}'

    def switch_points(self, points):
        pass

    # Scrape function using get_odds and get_teams.
    def scrape(self, url, name_index=None, timein=0.5, timeout=5, silent=False):
        self.driver.get(url)
        matches = self.driver.find_elements(By.CLASS_NAME, 'match-name-text')
        count_play = self.driver.page_source.count('In-Play') - 3
        for match_idx in range(count_play, len(matches)):
            # clicks on particular match
            self.driver.find_elements(By.CLASS_NAME, 'match-name-text')[match_idx].click()
            time.sleep(1)

            match_title = self.driver.find_element(By.CLASS_NAME, 'match-title').text
            team_dict = {match_title.split(' v ')[i]: match_title.split(' v ')[(i+1) % 2] for i in range(2)}

            # changes to SGM
            self.driver.find_elements(By.CLASS_NAME, 'tbc-tabular-item-link')[1].click()

            # turns off all categories
            for active_category in self.driver.find_elements(By.CLASS_NAME, '_1uszh93 '):
                self.scroll_click(active_category)

            # gets all legs
            category_dict = {i.text: i for i in self.driver.find_elements(By.CLASS_NAME, '_p1oke7 ')}
            leg_dict = {}
            for category in self.category_list:
                leg_dict[category] = {}
                # reset all categories and markets
                for active_category in self.driver.find_elements(By.CLASS_NAME, '_1uszh93 '):
                    self.scroll_click(active_category)
                category_dict[category].click()
                self.scroll_click(self.driver.find_element(By.CLASS_NAME, '_107y7tp '))

                # get all available markets
                market_dict = {i.text: i for i in self.driver.find_elements(By.CLASS_NAME, '_107y7tp ')}
                for market in self.market_list[category]:
                    self.scroll_click(market_dict[market])
                    time.sleep(1)
                    markets = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '_1k5b7ys ')] + [i.text for i in self.driver.find_elements(By.CLASS_NAME, '_ydwnsr ')]
                    odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '_njbycu ')]
                    leg_dict[category][market] = {markets[i]: odds[i] for i in range(len(markets))}
                    self.scroll_click(market_dict[market])

            # leg_1_list = [('Popular', 'Head To Head', i) for i in leg_dict['Popular']['Head To Head']]
# 'A Edwards Over 24.5 Pts'
# 'A Simons Over 22.5 Pts'
# 'Over 257.5'
            # Pick subset of legs for pick your own line
            close_odds = 1.15
            odds_list = abs(np.array([leg_dict['Popular']['Pick Your Own Line'][i] for i in leg_dict['Popular']['Pick Your Own Line']])-1.15)
            leg = list(leg_dict['Popular']['Pick Your Own Line'].keys())[np.argmin(odds_list)]
            odds = leg_dict['Popular']['Pick Your Own Line'][leg]
            leg_2_list = [('Popular', 'Pick Your Own Line', leg, odds)]
            alternate_line = self.switch_line(leg.split(' ')[-1])
            leg = f'''{team_dict[' '.join(leg.split(' ')[:-1])]} {alternate_line}'''
            leg_2_list.append(('Popular', 'Pick Your Own Line', leg, leg_dict['Popular']['Pick Your Own Line'][leg]))


            # Find alternate leg
            print(1)

            # Pick subset of legs for total points


            # Pick subset of legs for player points


            leg_1_list = [('Popular', 'Head To Head', i[0], i[1]) for i in leg_dict['Popular']['Head To Head']]
            leg_2_list = [('Popular', 'Pick Your Own Line', i[0], i[1]) for i in leg_dict['Popular']['Pick Your Own Line']]
            leg_3_list = [('Popular', 'Pick Your Own Total', i[0], i[1]) for i in leg_dict['Popular']['Pick Your Own Total']]
            leg_4_list = [('Player Points', 'Player Points', i[0], i[1]) for i in leg_dict['Player Points']['Player Points']]
            data_dict = {'Leg 1': [], 'Leg 2': [], 'Leg 3': [], 'Leg 4': [], 'Odds': []}
            for leg_1 in leg_1_list:
                self.click_leg(leg_1[0], leg_1[1], leg_1[2])
                for leg_2 in leg_2_list:
                    self.click_leg(leg_2[0], leg_2[1], leg_2[2])
                    for leg_3 in leg_3_list:
                        self.click_leg(leg_3[0], leg_3[1], leg_3[2])
                        for leg_4 in leg_4_list:
                            self.click_leg(leg_4[0], leg_4[1], leg_4[2])
                            odds = float(WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, '_ibw28o '))).text.replace(',', ''))
                            self.click_leg(leg_4[0], leg_4[1], leg_4[2])
                            data_dict['Leg 1'].append(leg_1[2])
                            data_dict['Leg 2'].append(leg_2[2])
                            data_dict['Leg 3'].append(leg_3[2])
                            data_dict['Leg 4'].append(leg_4[2])
                            data_dict['Odds'].append(odds)
            print(1)


    def write_to_csv(self):
        self.scrape('https://www.tab.com.au/sports/betting/Basketball/competitions/NBA')

if __name__ == "__main__":
    webscraper = WebScraper(None, False)
    webscraper.write_to_csv()