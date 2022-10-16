from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import re

class Topsport(WebScraper):
    def __init__(self, local):
        super().__init__(local)
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC', 'GAM Sports' : 'GAM'}

    def scrape_data(self):
        link = "https://www.topsport.com.au/Sport/Esports/League_of_Legends_-_Worlds_2022/Matches"
        self.driver.get(link)
        odds = [float(i) for i in re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)][:24]
        
        teams = [i for i in re.findall('''\\t([\w\. \d]+)\\n''', self.driver.page_source) if i != 'else'][:len(odds)]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Topsport(True)
    scrape_obj.write_to_csv()
