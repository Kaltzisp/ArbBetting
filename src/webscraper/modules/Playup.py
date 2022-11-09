from src.webscraper.WebScraper import WebScraper
import time
import re
import logging


class Playup(WebScraper):
    def __init__(self, driver, hidden):
        super().__init__(driver, hidden)
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
            link = "https://www.playup.com.au/betting/sports/mixed-martial-arts/ufc"
            self.driver.get(link)
            time.sleep(3)
            odds = re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)
            teams = [name.split(' ')[1] for name in re.findall('''pb-1 text-sm md:text-base">([\w\.\'\- ]*) <''', self.driver.page_source)]
            assert(len(teams) == len(odds))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
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
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]


if __name__ == "__main__":
    scrape_obj = Playup()
    scrape_obj.write_to_csv()
