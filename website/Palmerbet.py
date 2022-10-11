from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import time

class Palmerbet(WebScraper):
    def __init__(self, local):
        super().__init__(local)
        self.source = "Palmerbet"
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC'}

    def is_float(self, element) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    def scrape_data(self):
        link = "https://www.palmerbet.com/sports/esports/LoL%20-%20World%20Championship/a5150c01-0a8e-41d5-b2b6-f6638c7fcbb1"
        self.driver.get(link)
        while True:
            time.sleep(3)
            try:
                odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''ng-star-inserted''') if self.is_float(i.text)]
                break
            except:
                pass
        odds = odds[::3]
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''team-name''')]
        teams = [self.team_mapping[team] for team in teams]

        link = "https://www.palmerbet.com/sports/esports/LoL%20-%20World%20Championship/a5150c01-0a8e-41d5-b2b6-f6638c7fcbb1"
        self.driver.get(link)
        while True:
            time.sleep(3)
            try:
                odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''ng-star-inserted''') if self.is_float(i.text)]
                break
            except:
                pass
        odds = odds[::3]
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''team-name''')]
        teams = [self.team_mapping[team] for team in teams]

        link = "https://www.palmerbet.com/sports/martial-arts/Ultimate%20Fighting%20Championship/7ee8e39f-6bec-45c1-b484-28023ce0dfce"
        self.driver.get(link)
        while True:
            time.sleep(3)
            try:
                ufc_odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''ng-star-inserted''') if self.is_float(i.text)]
                break
            except:
                pass
        odds += ufc_odds[::3]
        ufc_names = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''team-name''')]
        teams += [name.split(",")[0] for name in ufc_names]

        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Palmerbet(True)
    scrape_obj.write_to_csv()
