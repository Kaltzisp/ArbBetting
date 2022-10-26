from src.WebScraper import WebScraper
from selenium.webdriver.common.by import By
import logging
import time


class Betfairback(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.team_mapping = {
            'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
            'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
            'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
            '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
            'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
            'LOUD': 'LLL', 'Jd Gaming': 'JDG', 'DRX': 'DRX', 'Royal Never Give Up': 'RNG',
            'Evil Geniuses': 'EG', 'Fnatic': 'FNC', 'Team Liquid': 'Team Liquid', 'Virtus.Pro': 'VP', 'Team Secret': 'Secret',
            'Xtreme Gaming': 'Xtreme Gaming'
        }

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
            link = "https://www.betfair.com.au/exchange/plus/e-sports/competition/10280189"
            self.driver.get(link)
            time.sleep(5)
            odds = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''bet-button-price''') if (self.is_float(i.text) or i.text == '')]
            for i, odd in enumerate(odds):
                if odd == '':
                    odds[i] = 0
            odds = [1+(float(odd)-1)*0.95 for (i, odd) in enumerate(odds) if i % 2 == 0]
            teams = [self.team_mapping[i.text] for i in self.driver.find_elements(By.CLASS_NAME, '''name''')]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('League import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.betfair.com.au/exchange/plus/en/mixed-martial-arts-betting-26420387"
            self.driver.get(link)
            time.sleep(5)
            odds = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''bet-button-price''') if (self.is_float(i.text) or i.text == '')]
            for i, odd in enumerate(odds):
                if odd == '':
                    odds[i] = 1
            odds = [1+(float(odd)-1)*0.95 for (i, odd) in enumerate(odds) if i % 2 == 0]
            teams = [i.text.split(' ')[-1] for i in self.driver.find_elements(By.CLASS_NAME, '''name''')]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('MMA import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.betfair.com.au/exchange/plus/basketball/competition/10547864"
            self.driver.get(link)
            time.sleep(5)
            odds = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''bet-button-price''') if (self.is_float(i.text) or i.text == '')]
            for i, odd in enumerate(odds):
                if odd == '':
                    odds[i] = 1
            odds = [1+(float(odd)-1)*0.95 for (i, odd) in enumerate(odds) if i % 2 == 0]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''name''')]
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
    scrape_obj = Betfairback()
    scrape_obj.write_to_csv()
