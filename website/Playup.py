from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import time
import re

class Playup(WebScraper):
    def __init__(self, local):
        super().__init__(local)
        self.source = "Playup"
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC', 'GAM Sports' : 'GAM'}

    def scrape_data(self):
        link = "https://www.playup.com.au/betting/sports/esports/lol-world-champs"
        self.driver.get(link)
        odds = re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)
        teams = re.findall('''pb-1 text-sm md:text-base">([\w\d\. ]*) <''', self.driver.page_source)
        teams = [self.team_mapping[team] for team in teams]


        link = "https://www.playup.com.au/betting/sports/mixed-martial-arts/ufc"
        self.driver.get(link)
        odds += re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)
        teams += re.findall('''pb-1 text-sm md:text-base">([\w\. ]*) <''', self.driver.page_source)

        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Playup(True)
    scrape_obj.write_to_csv()
