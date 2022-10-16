from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import re
import time

class Elitebet(WebScraper):
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
        link = '''https://www.elitebet.com.au/sports/Esports/League_of_Legends/ESPT'''
        self.driver.get(link)
        time.sleep(3)
        odds = [float(i) for i in re.findall('''css-147k6hk">&nbsp;<span>([\d\.]*)<''', self.driver.page_source)]
        teams = re.findall('''MuiTypography-root MuiTypography-body1 MuiTypography-alignCenter MuiTypography-noWrap css-1pex9yp">([\w\d\. ]*)<''', self.driver.page_source)
        teams = [self.team_mapping[team] for team in teams]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Elitebet(True)
    scrape_obj.write_to_csv()
