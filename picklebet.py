from webscraper import WebScraper
from selenium.webdriver.common.by import By

class Picklebet(WebScraper):
    def __init__(self):
        super().__init__()
        self.source = "Picklebet"
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                'CTBC Flying Oyster': 'CFO', 'T1 Esports': 'T1', 'EDward Gaming': 'EDG',
                'Top Esports': 'TES', 'DAMWON Gaming': 'DK', 'GAM Esports': 'GAM',
                '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX':'DRX', 'Royal Never Give Up':'RNG',
                'Evil Geniuses': 'EG', 'Fnatic': 'FNC'}

    def scrape_data(self):
        link = "https://picklebet.com/?game=lol"
        self.driver.get(link)
        self.driver.find_element(By.XPATH, '''//*[@id="gatsby-focus-wrapper"]/div[2]/div[2]/div/main/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/button[2]/span''').click()

        odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''Outcome-module--odds--onB1v''')]
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''Outcome-module--name--DgQM8''')]
        teams = [self.team_mapping[team] for team in teams]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Picklebet()
    scrape_obj.write_to_csv()
