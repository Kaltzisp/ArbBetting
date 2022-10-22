from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import logging
import traceback
class Sportsbet(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                        'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
                        'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
                        '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                        'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                        'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
                        'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC'}

    def scrape_data(self):
        total_odds = []
        total_teams = []
        try:
            link = "https://www.sportsbet.com.au/betting/e-sports/lol-world-championship"
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.XPATH, '''//span[@class='size14_f7opyze bold_f1au7gae priceTextSize_frw9zm9']''')]
            teams = [i.text for i in self.driver.find_elements(By.XPATH, '''//span[@class='size12_fq5j3k2 normal_fgzdi7m caption_f4zed5e']''')]
            teams = [self.team_mapping[team] for team in teams]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('League of Legends import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.sportsbet.com.au/betting/ufc-mma"
            self.driver.get(link)
            try:
                self.driver.find_element(By.XPATH, '''/html/body/div[3]/div/div/div/div/div[3]/div/button/div/span''').click()
            except:
                pass
            odds =[float(i.text) for i in self.driver.find_elements(By.XPATH, '''//span[@class='size14_f7opyze bold_f1au7gae priceTextSize_frw9zm9']''')]
            ufc_names = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''size12_fq5j3k2''')][2:]
            teams = [name.split(' ')[1] for name in ufc_names]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.sportsbet.com.au/betting/basketball-us"
            self.driver.get(link)
            odds =[float(i.text) for i in self.driver.find_elements(By.XPATH, '''//span[@class='size14_f7opyze bold_f1au7gae priceTextSize_frw9zm9']''')]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''size12_fq5j3k2''')][2:]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.info(traceback.format_exc())
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]

if __name__ == "__main__":
    scrape_obj = Sportsbet()
    scrape_obj.write_to_csv()
