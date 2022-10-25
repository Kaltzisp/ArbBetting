from src.WebScraper import WebScraper
from selenium.webdriver.common.by import By
import logging
import time


class Betdeluxe(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)

    def is_float(self, element) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    def scrape_data(self):
        total_odds = []
        total_teams = []
        try:
            link = "https://www.betdeluxe.com.au/sports/basketball/nba-1000059"
            self.driver.get(link)
            time.sleep(1)
            odds = [i.text for i in self.driver.find_elements(By.ID, '''multiBet''') if self.is_float(i.text)][::3]
            odds = [float(i) for i in odds]
            teams = [i.text for i in self.driver.find_elements(By.ID, '''multiBet''') if ((not self.is_float(i.text)) & (i.text != ''))]
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
    scrape_obj = Betdeluxe()
    scrape_obj.write_to_csv()
