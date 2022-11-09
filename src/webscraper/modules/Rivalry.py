from src.webscraper.WebScraper import WebScraper
from selenium.webdriver.common.by import By
import logging


class Rivalry(WebScraper):
    def __init__(self, driver, hidden):
        super().__init__(driver, hidden)
        self.team_mapping = {
            'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
            'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'EDward Gaming': 'EDG',
            'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
            '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
            'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
            'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
            'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC', 'GAM Sports': 'GAM'
        }

    def scrape_data(self):
        total_odds = []
        total_teams = []

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
            logging.exception(e)
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
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]


if __name__ == "__main__":
    scrape_obj = Rivalry()
    scrape_obj.write_to_csv()
