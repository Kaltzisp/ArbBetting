from webscraper import WebScraper
from selenium.webdriver.common.by import By
import re
import logging
import traceback
class Topsport(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
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
            link = "https://www.topsport.com.au/Sport/Esports/League_of_Legends_-_Worlds_2022/Matches"
            self.driver.get(link)
            odds = [float(i) for i in re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)][:8]
            teams = [i for i in re.findall('''\\t([\w\. \d]+)\\n''', self.driver.page_source) if i != 'else'][:len(odds)]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('League of Legends import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]

if __name__ == "__main__":
    scrape_obj = Topsport()
    scrape_obj.write_to_csv()
