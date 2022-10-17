from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import logging
import traceback
import re
class Pointsbet(WebScraper):
    def __init__(self):
        super().__init__()
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX':'DRX', 'Royal Never Give Up':'RNG',
                'Evil Geniuses': 'EG', 'Fnatic': 'FNC', 'Team Liquid': 'Team Liquid', 'Virtus.Pro': 'VP', 'Team Secret': 'Secret', 
                'Xtreme Gaming': 'Xtreme Gaming'}

    def scrape_data(self):
        total_odds = []
        total_teams = []

        try:
            link = "https://pointsbet.com.au/sports/e-sports/[LoL]-World-Championship"
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''fheif50''')]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''f5rl2hl''')]
            teams = [self.team_mapping[team] for team in teams]
            assert(len(teams) == len(odds))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('League of Legends import failed')
        total_odds += odds
        total_teams += teams

        # link = "https://pointsbet.com.au/sports/e-sports/[DOTA]-The-International"
        # self.driver.get(link)
        # odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''fheif50''')]
        # teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''f5rl2hl''')]
        # teams = [self.team_mapping[team] for team in teams]
        try:
            link = "https://pointsbet.com.au/sports/mma/UFC"
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''fheif50''')]
            ufc_names = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''f5rl2hl''')]
            teams = [name.split( )[1] for name in ufc_names]
            assert(len(teams) == len(odds))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://pointsbet.com.au/sports/basketball/NBA"
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''fheif50''')][::3]
            teams = re.findall('''feu1e1k fyraa0v f1qmefvr">([\w\.\'\- ]*)<''', self.driver.page_source)
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
    scrape_obj = Pointsbet()
    scrape_obj.write_to_csv()
