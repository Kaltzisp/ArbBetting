from src.webscraper.WebScraper import WebScraper
from selenium.webdriver.common.by import By
import logging


class Ladbrokes(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)

    def scrape_data(self):
        total_odds = []
        total_teams = []

        try:
            link = "https://www.ladbrokes.com.au/sports/mma"
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''price-button-odds''')]
            teams = [i.text.split(' ')[1] for i in self.driver.find_elements(By.CLASS_NAME, '''displayTitle''')]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = "https://www.ladbrokes.com.au/sports/basketball/usa/nba"
            self.driver.get(link)
            odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''price-button-odds''')]
            teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''displayTitle''')]
            lines = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''displayLine''') if i.text != '']
            odds = odds[:len(odds)-len(lines)]
            teams = teams[:len(teams)-len(lines)]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]

        # n_game_elements = len([i for i in self.driver.find_elements(By.CLASS_NAME, '''sports-event-title__name-text''')])
        # for idx in range(n_game_elements):
        #     game = self.driver.find_elements(By.CLASS_NAME, '''sports-event-title__name-text''')[idx]
        #     game.click()
        #     self.driver.find_element(By.XPATH, '''//*[@id="25bf3cd2-c56e-4b41-8a73-ccad21982ab3"]/div[1]/h3/span''').click()
        #     self.driver.find_element(By.XPATH, '''//*[@id="f58b187d-939e-448f-8e0c-b9c216c959d3"]/div[1]/h3/span''').click()
        #     self.driver.find_element(By.XPATH, '''//*[@id="77d78111-48ba-4c5e-b605-d4ad29f5b441"]/div[1]/h3/span''').click()
        #     first_blood_id = re.findall('''id="(accordion_[\w\d]{8}-[\w\d]{4}-[\w\d]{4}-[\w\d]{4}-[\w\d]{12})"[^<>]*> <[^<>]*><[^<>]*> <[^<>]*><[^<>]*>First Blood<''', self.driver.page_source)[0]
        #     first_inhib_id = re.findall('''id="(accordion_[\w\d]{8}-[\w\d]{4}-[\w\d]{4}-[\w\d]{4}-[\w\d]{12})"[^<>]*> <[^<>]*><[^<>]*> <[^<>]*><[^<>]*>Team to destroy First Inhibitor<''', self.driver.page_source)[0]
        #     self.driver.find_element(By.XPATH, f'''//*[@id="{first_blood_id}"]/div[1]/h3/span''').click()
        #     self.driver.find_element(By.XPATH, f'''//*[@id="{first_inhib_id}"]/div[1]/h3/span''').click()
        #     odds += [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''price-button-odds''') if i.text != ''][2:]
        #     teams += [i.text + ' First Inhib' for i in self.driver.find_elements(By.CLASS_NAME, '''market-two-col__entrant-name''') if i.text != ''][:2]
        #     teams += [i.text + ' First Blood' for i in self.driver.find_elements(By.CLASS_NAME, '''market-two-col__entrant-name''') if i.text != ''][2:4]
        #     self.driver.back()


if __name__ == "__main__":
    scrape_obj = Ladbrokes()
    scrape_obj.write_to_csv()
