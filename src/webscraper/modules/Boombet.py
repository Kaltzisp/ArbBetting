from src.webscraper.WebScraper import WebScraper
import re
import logging
import time


class Boombet(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.team_mapping = {
            'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
            'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
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
            link = '''https://www.boombet.com.au/sport-menu/Sport/Mixed%20Martial%20Arts/UFC'''
            self.driver.get(link)
            time.sleep(1)
            odds = [float(i) for i in re.findall('''oddsValue d-block d-md-flex">([\d\.]*)<''', self.driver.page_source)]
            teams = re.findall('''teamName d-block d-md-flex pb-1">([\w\d\.\-' ]*)<''', self.driver.page_source)
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
            link = '''https://www.boombet.com.au/sport-menu/Sport/Basketball/US%20NBA%20Regular%20Season-22'''
            self.driver.get(link)
            time.sleep(1)
            odds = [float(i) for i in re.findall('''oddsValue d-block d-md-flex">([\d\.]*)<''', self.driver.page_source)]
            teams = re.findall('''teamName d-block d-md-flex pb-1">([\w\d\.\-' ]*)<''', self.driver.page_source)
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
    scrape_obj = Boombet()
    scrape_obj.write_to_csv()
