<<<<<<< HEAD:src/modules/Betr.py
from src.WebScraper import WebScraper
import re
import time
import logging


=======
from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import re
import time
import logging
import traceback
>>>>>>> master:website/Betr.py
class Betr(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)

    def scrape_data(self):
        total_odds = []
        total_teams = []

<<<<<<< HEAD:src/modules/Betr.py
        try:
=======
        try:    
>>>>>>> master:website/Betr.py
            link = '''https://betr.com.au/sportsbook#/sport/13/competition/1000649/1003042'''
            self.driver.get(link)
            time.sleep(1)
            odds = [float(i) for i in re.findall('''span>([\d\.]+)<''', self.driver.page_source)]
            teams = re.findall('''OddsButton_priceType__ROL\+V">([\w\d\. ]*)<''', self.driver.page_source)
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
<<<<<<< HEAD:src/modules/Betr.py
            logging.exception(e)
=======
            logging.info(traceback.format_exc())
>>>>>>> master:website/Betr.py
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

<<<<<<< HEAD:src/modules/Betr.py
        try:
=======
        try:    
>>>>>>> master:website/Betr.py
            link = '''https://betr.com.au/sportsbook#/sport/9/competition/1000226/1000520'''
            self.driver.get(link)
            time.sleep(1)

            odds = [float(i) for i in re.findall('''span>([\d\.]+)<''', self.driver.page_source)]
            teams = [team.split(' ')[-1] for team in re.findall('''OddsButton_priceType__ROL\+V">([\w\d\. ]*)<''', self.driver.page_source)]

            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
<<<<<<< HEAD:src/modules/Betr.py
            logging.exception(e)
=======
            logging.info(traceback.format_exc())
>>>>>>> master:website/Betr.py
            logging.info('MMA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]

<<<<<<< HEAD:src/modules/Betr.py

=======
>>>>>>> master:website/Betr.py
if __name__ == "__main__":
    scrape_obj = Betr()
    scrape_obj.write_to_csv()
