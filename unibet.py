from webscraper import WebScraper
from selenium.webdriver.common.by import By
import time

class Unibet(WebScraper):
    def __init__(self):
        super().__init__()
        self.source = "Unibet"
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG'}

    def scrape_data(self):
        link = "https://www.unibet.com.au/betting/sports/filter/esports/league_of_legends/world_championship/all/matches"
        self.driver.get(link)
        self.driver.find_element(By.XPATH, '''//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]''').click()
        while True:
            try:
                odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''_8e013''')]
                break
            except:
                time.sleep(3)
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''c539a''')]

        teams = [self.team_mapping[team] for team in teams]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Unibet()
    scrape_obj.write_to_csv()
