from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import re

class Betright(WebScraper):
    def __init__(self):
        super().__init__()
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC', 'GAM Sports' : 'GAM'}

    def scrape_data(self):
        link = '''https://www.betright.com.au/sports/Esports/League-of-Legends/World-Championship/14468'''
        self.driver.get(link)
        odds = [float(i) for i in re.findall('''place-bet__odds ng-binding">([\d\.]*)<''', self.driver.page_source)]
        teams = re.findall('''zeta  headline-wrap ng-binding">([\w\d\. ]*)<''', self.driver.page_source)
        teams = [self.team_mapping[team] for team in teams]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Betright()
    scrape_obj.write_to_csv()
