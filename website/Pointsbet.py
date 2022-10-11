from website.webscraper import WebScraper
from selenium.webdriver.common.by import By

class Pointsbet(WebScraper):
    def __init__(self, local):
        super().__init__(local)
        self.source = "Pointsbet"
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX':'DRX', 'Royal Never Give Up':'RNG',
                'Evil Geniuses': 'EG', 'Fnatic': 'FNC', 'Team Liquid': 'Team Liquid', 'Virtus.Pro': 'VP', 'Team Secret': 'Secret', 
                'Xtreme Gaming': 'Xtreme Gaming'}

    def scrape_data(self):
        # link = "https://pointsbet.com.au/sports/e-sports/[LoL]-World-Championship"
        # self.driver.get(link)
        # odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''fheif50''')]
        # teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''f5rl2hl''')]
        # teams = [self.team_mapping[team] for team in teams]

        link = "https://pointsbet.com.au/sports/e-sports/[DOTA]-The-International"
        self.driver.get(link)
        odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''fheif50''')]
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''f5rl2hl''')]
        teams = [self.team_mapping[team] for team in teams]

        link = "https://pointsbet.com.au/sports/mma/UFC"
        self.driver.get(link)
        odds += [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''fheif50''')]
        ufc_names = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''f5rl2hl''')]
        teams += [name.split( )[1] for name in ufc_names]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Pointsbet(True)
    scrape_obj.write_to_csv()
