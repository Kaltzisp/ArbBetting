from selenium.webdriver.common.by import By
from website.webscraper import WebScraper
import re
import logging
import traceback
class Rivalry(WebScraper):
    def __init__(self):
        super().__init__()
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'EDward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC', 'GAM Sports' : 'GAM'}

    def scrape_data(self):
        total_odds = []
        total_teams = []
        try:
            link = '''https://www.rivalry.com/au/esports/league-of-legends-betting/2753-world-championship'''
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''outcome-odds''')]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''outcome-name''')]
            teams = [self.team_mapping[team] for team in teams]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('League of Legends import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = '''https://www.rivalry.com/au/sports/mma-betting'''
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''outcome-odds''')]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''outcome-name''')]
            teams = [team.split(' ')[-1] for team in teams]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = '''https://www.rivalry.com/au/sports/basketball-betting/3378-nba'''
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''outcome-odds''')]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''outcome-name''')]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]

if __name__ == "__main__":
    scrape_obj = Rivalry()
    scrape_obj.write_to_csv()
