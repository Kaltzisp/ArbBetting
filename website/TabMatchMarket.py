from webscraper import WebScraper
from selenium.webdriver.common.by import By

class TabMatchMarket(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2': 'G2',
                'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'EDward Gaming': 'EDG',
                'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM': 'GAM',
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
        odds = odds[len(odds)//2:]
        teams = [i.text[:-4] for i in self.driver.find_elements(By.CLASS_NAME, '''proposition-title''') if len(i.text) != 0]
        teams = [self.team_mapping[team] for team in teams]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = TabMatchMarket()
    scrape_obj.write_to_csv()
