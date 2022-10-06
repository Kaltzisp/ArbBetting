from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import time
import re

class Playup(WebScraper):
    def __init__(self):
        super().__init__()
        self.source = "Playup"
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC'}

    def scrape_data(self):
        link = "https://www.playup.com.au/betting/sports/esports/lol-world-champs"
        self.driver.get(link)
        # use regex to obtain odds
        odds = re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)
        teams = re.findall('''pb-1 text-sm md:text-base">([\w\d\. ]*) <''', self.driver.page_source)
        teams = [self.team_mapping[team] for team in teams]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Playup()
    scrape_obj.write_to_csv()
