from src.webscraper.WebScraper import WebScraper
import re
import time
import logging
from selenium.webdriver.common.by import By

class Betnation(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)

    def scrape_data(self):
        total_odds = []
        total_teams = []

        try:
            link = '''https://betnation.com.au/sports/basketball/nba-1000003'''
            self.driver.get(link)
            time.sleep(1)
            data = [i.text for i in self.driver.find_elements(By.ID, '''multiBet''') if i.text != '']
            odds = [float(i) for i in data[1::4]]
            teams = [i for i in data[::4]]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = '''https://betnation.com.au/sports/martial-arts-ufc/ultimate-fighting-championship-1000311'''
            self.driver.get(link)
            time.sleep(1)
            data = [i.text for i in self.driver.find_elements(By.ID, '''multiBet''') if i.text != '']
            odds = [float(i) for i in data[1::4]]
            teams = [i.split(', ')[0] for i in data[::4]]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('MMA import failed')
        total_odds += odds
        total_teams += teams
        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]


if __name__ == "__main__":
    scrape_obj = Betnation()
    scrape_obj.write_to_csv()
