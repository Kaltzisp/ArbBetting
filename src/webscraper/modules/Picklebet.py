from src.webscraper.WebScraper import WebScraper
from selenium.webdriver.common.by import By
import logging


class Picklebet(WebScraper):
    def __init__(self, driver, hidden):
        super().__init__(driver, hidden)
        self.team_mapping = {
            'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
            'CTBC Flying Oyster': 'CFO', 'T1 Esports': 'T1', 'EDward Gaming': 'EDG',
            'Top Esports': 'TES', 'DAMWON Gaming': 'DK', 'GAM Esports': 'GAM',
            '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
            'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
            'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Royal Never Give Up': 'RNG',
            'Evil Geniuses': 'EG', 'Fnatic': 'FNC', 'Team Secret': 'Secret', 'Virtus.Pro': 'VP'
        }

    def scrape_data(self):
        total_odds = []
        total_teams = []

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
            logging.exception(e)
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
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]


if __name__ == "__main__":
    scrape_obj = Picklebet()
    scrape_obj.write_to_csv()
