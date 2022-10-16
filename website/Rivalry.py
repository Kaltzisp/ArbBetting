from selenium.webdriver.common.by import By
from website.webscraper import WebScraper
import re

class Rivalry(WebScraper):
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
        link = '''https://www.rivalry.com/au/esports/league-of-legends-betting/2753-world-championship'''
        self.driver.get(link)
        odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''outcome-odds''')]
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''outcome-name''')]
        teams = [self.team_mapping[team] for team in teams]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Rivalry()
    scrape_obj.write_to_csv()
