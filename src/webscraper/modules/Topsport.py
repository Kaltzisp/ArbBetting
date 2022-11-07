from src.webscraper.WebScraper import WebScraper
import re
import logging
from selenium.webdriver.common.by import By
import time

class Topsport(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.team_mapping = {
            'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
            'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
            'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
            '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
            'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
            'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
            'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC', 'GAM Sports': 'GAM'
        }

    def scrape_data(self):
        total_odds = []
        total_teams = []
        try:
            link = "https://www.topsport.com.au/Sport/Upcoming"
            self.driver.get(link)
            self.driver.find_element(By.XPATH, '''//*[@id="NavAreaSports"]''').click()
            self.driver.find_element(By.XPATH, '''//*[@id="22"]/a''').click()
            odds = []
            teams = []
            count = 1
            id = re.findall('''(widget_SportMenu-\d+)''', self.driver.page_source)[0]
            while True:
                try:
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, f'''//*[@id="{id}"]/dl/dd[18]/dl/dd/ul/li[{count}]''').click()
                    time.sleep(2)
                    sub_odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''oddsColumn''') if i.text not in ['', 'Win']]
                    sub_teams = [i[0].split(' ')[-1] for i in re.findall('''<td>([\w\.\'\- ]+)<\/td|\\t([\w\.\'\- ]+)\\n''', self.driver.page_source) if i[1] == '']
                    assert(len(sub_odds) == len(sub_teams))
                    odds += sub_odds
                    teams += sub_teams
                    count += 1
                except Exception as e:
                    sub_odds = []
                    sub_teams = []
                    break
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('MMA import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.topsport.com.au/Sport/Basketball/NBA_Matches/Matches"
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''oddsColumn''') if ((i.text not in ['O/U', '', 'Win','Line']) and ('@' not in i.text))]
            teams = [i[0] for i in re.findall('''<td>([\w\.\'\- ]+)<\/td|\\t([\w\.\'\- ]+)\\n''', self.driver.page_source) if i != ('', 'else')]
            teams = teams[:len(odds)]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]


if __name__ == "__main__":
    scrape_obj = Topsport()
    scrape_obj.write_to_csv()
