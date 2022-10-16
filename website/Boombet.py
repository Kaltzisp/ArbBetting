from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import re

class Boombet(WebScraper):
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
        link = '''https://www.boombet.com.au/sport-menu/Sport/Esports/League%20of%20Legends'''
        self.driver.get(link)
        odds = [float(i) for i in re.findall('''oddsValue d-block d-md-flex">([\d\.]*)<''', self.driver.page_source)]
        teams = re.findall('''teamName d-block d-md-flex pb-1">([\w\d\. ]*)<''', self.driver.page_source)
        teams = [self.team_mapping[team] for team in teams]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Boombet()
    scrape_obj.write_to_csv()
