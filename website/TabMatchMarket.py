from website.webscraper import WebScraper
from selenium.webdriver.common.by import By

class TabH2H(WebScraper):
    def __init__(self, local):
        super().__init__(local)
        self.source = "Picklebet"
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                'CTBC Flying Oyster': 'CFO', 'T1 Esports': 'T1', 'EDward Gaming': 'EDG',
                'Top Esports': 'TES', 'DAMWON Gaming': 'DK', 'GAM Esports': 'GAM',
                '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX':'DRX', 'Royal Never Give Up':'RNG',
                'Evil Geniuses': 'EG', 'Fnatic': 'FNC', 'Gam': 'GAM', 'Gen.g': 'GEN','Edward Gaming': 'EDG',
                'Royal Never Give':'RNG'}

    def scrape_data(self):
        link = "https://www.tab.com.au/sports/betting/Esports/competitions/League%20of%20Legends/tournaments/LoL%20-%20World%20Championships"
        self.driver.get(link)
        self.driver.find_element(By.XPATH, '''//*[@id="correct_score"]/h3/div/span''').click()
        odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''animate-odd''')]
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''match-name-text''')]
        teams = [self.team_mapping[team] for team in teams]

if __name__ == "__main__":
    scrape_obj = TabH2H(True)
    scrape_obj.write_to_csv()

