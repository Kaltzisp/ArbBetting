from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import time
import re
import logging
import traceback
class Playup(WebScraper):
    def __init__(self):
        super().__init__()
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC', 'GAM Sports' : 'GAM'}

    def scrape_data(self):
        total_odds = []
        total_teams = []

        try:
            link = "https://www.playup.com.au/betting/sports/esports/lol-world-champs"
            self.driver.get(link)
            odds = re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)
            teams = re.findall('''pb-1 text-sm md:text-base">([\w\d\. ]*) <''', self.driver.page_source)
            teams = [self.team_mapping[team] for team in teams]
            assert(len(teams) == len(odds))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('League of Legends import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.playup.com.au/betting/sports/mixed-martial-arts/ufc"
            self.driver.get(link)
            time.sleep(3)
            odds = re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)
            teams = [name.split(' ')[1] for name in re.findall('''pb-1 text-sm md:text-base">([\w\.\'\- ]*) <''', self.driver.page_source)]
            assert(len(teams) == len(odds))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.playup.com.au/betting/sports/basketball/nba"
            self.driver.get(link)
            time.sleep(3)
            odds = [float(i) for i in re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)]
            teams = re.findall('''pb-1 text-sm md:text-base">([\w\.\'\- ]*) <''', self.driver.page_source)
            assert(len(teams) == len(odds))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]

if __name__ == "__main__":
    scrape_obj = Playup()
    scrape_obj.write_to_csv()
