
from webscraper import WebScraper
from selenium.webdriver.common.by import By
import time
import logging
import traceback
class Palmerbet(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC'}

    def is_float(self, element) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    def scrape_data(self):
        total_odds = []
        total_teams = []

        try:
            link = "https://www.palmerbet.com/sports/esports/LoL%20-%20World%20Championship/a5150c01-0a8e-41d5-b2b6-f6638c7fcbb1"
            self.driver.get(link)
            while True:
                time.sleep(3)
                try:
                    odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''ng-star-inserted''') if self.is_float(i.text)]
                    break
                except:
                    pass
            odds = odds[::3]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''team-name''')]
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
            link = "https://www.palmerbet.com/sports/martial-arts/Ultimate%20Fighting%20Championship/7ee8e39f-6bec-45c1-b484-28023ce0dfce"
            self.driver.get(link)
            while True:
                time.sleep(3)
                try:
                    ufc_odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''ng-star-inserted''') if self.is_float(i.text)]
                    break
                except:
                    pass
            odds = ufc_odds[::3]
            ufc_names = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''team-name''')]
            teams = [name.split(",")[0] for name in ufc_names]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = '''https://www.palmerbet.com/sports/basketball/NBA/b26e5acc-02ff-4b22-ae69-0491fbd2500e'''
            self.driver.get(link)
            while True:
                time.sleep(3)
                try:
                    odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''ng-star-inserted''') if self.is_float(i.text)]
                    break
                except:
                    pass
            odds = odds[::3]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''team-name''')]
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
    scrape_obj = Palmerbet()
    scrape_obj.write_to_csv()
