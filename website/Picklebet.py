from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import logging
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
class Picklebet(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                'CTBC Flying Oyster': 'CFO', 'T1 Esports': 'T1', 'EDward Gaming': 'EDG',
                'Top Esports': 'TES', 'DAMWON Gaming': 'DK', 'GAM Esports': 'GAM',
                '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX':'DRX', 'Royal Never Give Up':'RNG',
                'Evil Geniuses': 'EG', 'Fnatic': 'FNC', 'Team Secret': 'Secret', 'Virtus.Pro': 'VP'}

    def scrape_data(self):
        total_odds = []
        total_teams = []

        try:
            link = "https://picklebet.com/?game=lol"
            self.driver.get(link)
            self.driver.find_element(By.XPATH, '''//*[@id="gatsby-focus-wrapper"]/div[2]/div[2]/div/main/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/button[2]/span''').click()
            odds = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''Outcome-module--odds--onB1v''')]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''Outcome-module--name--DgQM8''')]

            for i, odd in enumerate(odds):
                if odd != '-':
                    break
            odds = [float(j) for j in odds[i:]]
            teams = teams[i:]
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
            link = "https://picklebet.com/sports/mma/betting?page=1&tab=next"
            self.driver.get(link)
            MMAPickleteams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''Outcome-module--name--DgQM8''')]
            teams = []
            for team in MMAPickleteams:
                Name = team.split(", ")
                Name = Name[0]
                teams.append(Name)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''Outcome-module--odds--onB1v''')]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://picklebet.com/sports/basketball/betting?page=1&tab=next&tour=BASKETBALL%3ANBA"
            self.driver.get(link)
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''Outcome-module--name--DgQM8''')]
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''Outcome-module--odds--onB1v''')]
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
    scrape_obj = Picklebet()
    scrape_obj.write_to_csv()
