from src.webscraper.WebScraper import WebScraper
import re
import time
import logging


class Elitebet(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
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
            link = '''https://www.elitebet.com.au/sports/Basketball/NBA/BASK'''
            self.driver.get(link)
            time.sleep(3)
            odds = [float(i) for i in re.findall('''css-147k6hk">&nbsp;<span>([\d\.]*)<''', self.driver.page_source)]
            teams = re.findall('''MuiTypography-root MuiTypography-body1 MuiTypography-alignCenter MuiTypography-noWrap css-1pex9yp">([\w\d\. ]*)<''', self.driver.page_source)
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = '''https://www.elitebet.com.au/sports/Mixed_Martial_Arts/MMA'''
            self.driver.get(link)
            time.sleep(3)
            odds = [float(i) for i in re.findall('''css-147k6hk">&nbsp;<span>([\d\.]*)<''', self.driver.page_source)]
            teams = re.findall('''MuiTypography-root MuiTypography-body1 MuiTypography-alignCenter MuiTypography-noWrap css-1pex9yp">([\w\d\. ]*)<''', self.driver.page_source)
            teams = [team.split(' ')[-1] for team in teams]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]


if __name__ == "__main__":
    scrape_obj = Elitebet()
    scrape_obj.write_to_csv()
