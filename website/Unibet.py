from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import time

class Unibet(WebScraper):
    def __init__(self, local):
        super().__init__(local)
        self.source = "Unibet"
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC'}

    def scrape_data(self):
        link = "https://www.unibet.com.au/betting/sports/filter/esports/league_of_legends/world_championship/all/matches"
        self.driver.get(link)
        self.driver.find_element(By.XPATH, '''//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]''').click()
        time.sleep(3)
        odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''_8e013''')]
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''c539a''')]
        if len(teams)-4 == len(odds):
            teams = teams[2:]
            teams = teams[:4] + teams[6:]
        teams = [self.team_mapping[team] for team in teams]


        link = "https://www.unibet.com.au/betting/sports/filter/ufc_mma/all/matches"
        self.driver.get(link)
        time.sleep(3)
        odds += [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''_8e013''')]
        UFCUnibetteams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''c539a''')]

        for team in UFCUnibetteams:
            if ',' in team:
                Name = team.split(", ")
                Name = Name[0]
            else: 
                Name = team
            teams.append(Name)

        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Unibet(True)
    scrape_obj.write_to_csv()
