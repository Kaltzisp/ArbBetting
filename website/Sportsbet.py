from website.webscraper import WebScraper
from selenium.webdriver.common.by import By

class Sportsbet(WebScraper):
    def __init__(self):
        super().__init__()
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC'}

    def scrape_data(self):
        link = "https://www.sportsbet.com.au/betting/e-sports/lol-world-championship"
        self.driver.get(link)
        odds = [float(i.text) for i in self.driver.find_elements(By.XPATH, '''//span[@class='size14_f7opyze bold_f1au7gae priceTextSize_frw9zm9']''')]
        teams = [i.text for i in self.driver.find_elements(By.XPATH, '''//span[@class='size12_fq5j3k2 normal_fgzdi7m caption_f4zed5e']''')]

        teams = [self.team_mapping[team] for team in teams]


        link = "https://www.sportsbet.com.au/betting/ufc-mma"
        self.driver.get(link)
        odds += [float(i.text) for i in self.driver.find_elements(By.XPATH, '''//span[@class='size14_f7opyze bold_f1au7gae priceTextSize_frw9zm9']''')]
        ufc_names = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''size12_fq5j3k2''')][4:]
        teams += [name.split(' ')[1] for name in ufc_names]

        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Sportsbet()
    scrape_obj.write_to_csv()
