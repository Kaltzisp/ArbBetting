from src.WebScraper import WebScraper
from selenium.webdriver.common.by import By
import time
import logging


class Unibet(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.team_mapping = {
            'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
            'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
            'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
            '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
            'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
            'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
            'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC'
        }

    def scrape_data(self):
        total_odds = []
        total_teams = []
        try:
            link = "https://www.unibet.com.au/betting/sports/filter/esports/league_of_legends/world_championship/all/matches"
            self.driver.get(link)
            self.driver.find_element(By.XPATH, '''//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]''').click()
            time.sleep(3)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''_8e013''')]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''c539a''')]
            if len(teams) - 4 == len(odds):
                teams = teams[2:]
                teams = teams[:4] + teams[6:]
            teams = [self.team_mapping[team] for team in teams]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('League of Legends import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.unibet.com.au/betting/sports/filter/ufc_mma/all/matches"
            teams = []
            self.driver.get(link)
            time.sleep(3)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''_8e013''')]
            UFCUnibetteams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''c539a''')]

            for team in UFCUnibetteams:
                if ',' in team:
                    Name = team.split(", ")
                    Name = Name[0]
                else:
                    Name = team
                teams.append(Name)
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.unibet.com.au/betting/sports/filter/basketball/nba/all/matches"
            self.driver.get(link)
            time.sleep(3)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''_8e013''')]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''c539a''')]
            if len(teams) - 4 == len(odds):
                teams = teams[2:]
                teams = teams[:4] + teams[6:]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]


if __name__ == "__main__":
    scrape_obj = Unibet()
    scrape_obj.write_to_csv()
