from website.webscraper import WebScraper
from selenium.webdriver.common.by import By

class Ladbrokes(WebScraper):
    def __init__(self, local):
        super().__init__(local)

    def scrape_data(self):
        link = "https://www.ladbrokes.com.au/sports/esports/lo-l-worlds"
        self.driver.get(link)
        odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''price-button-odds''')]
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''displayTitle''')]

        # game_elements = [i for i in self.driver.find_elements(By.CLASS_NAME, '''sports-event-title__name-text''')]
        # for game in game_elements:
        #     game.click()
        #     self.driver.find_element(By.XPATH, '''//*[@id="25bf3cd2-c56e-4b41-8a73-ccad21982ab3"]/div[1]/h3/span''').click()
        #     self.driver.find_element(By.XPATH, '''//*[@id="f58b187d-939e-448f-8e0c-b9c216c959d3"]/div[1]/h3/span''').click()
        #     self.driver.find_element(By.XPATH, '''//*[@id="77d78111-48ba-4c5e-b605-d4ad29f5b441"]/div[1]/h3/span''').click()
        #     self.driver.find_element(By.CSS_SELECTOR, '''#accordion_3403c965-362f-44ab-b013-ce89925d4538 > div.accordion__title.accordion-markets-nested__title.not-first-child.collapsed > h3 > span''').click()
        #     self.driver.find_element(By.XPATH, '''//*[@id="accordion_35202b8b-2af0-4e0b-9023-6cbfe355d8b1"]/div[1]/h3/span''').click()
        #     odds += [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''price-button-odds''') if i.text != ''][2:]
        #     teams += [i.text + ' First Inhib' for i in self.driver.find_elements(By.CLASS_NAME, '''market-two-col__entrant-name''') if i.text != ''][:2]
        #     teams += [i.text + ' First Blood' for i in self.driver.find_elements(By.CLASS_NAME, '''market-two-col__entrant-name''') if i.text != ''][2:4]
        #     self.driver.back()

        link = "https://www.ladbrokes.com.au/sports/mma"
        self.driver.get(link)
        odds += [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''price-button-odds''')]
        teams += [i.text.split(' ')[1] for i in self.driver.find_elements(By.CLASS_NAME, '''displayTitle''')]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Ladbrokes(True)
    scrape_obj.write_to_csv()
