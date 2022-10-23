from webscraper import WebScraper
from selenium.webdriver.common.by import By

class Neds(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)

    def scrape_data(self):
        link = "https://www.neds.com.au/sports/esports/lo-l-worlds"
        self.driver.get(link)
        odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''price-button-odds''')]
        teams = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''displayTitle''')]

        link = "https://www.neds.com.au/sports/mma"
        self.driver.get(link)
        odds += [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''price-button-odds''')]
        UpperCaseteam = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''displayTitle''')]
        for team in UpperCaseteam:
                TeamName = team.title()
                teams.append(TeamName.split(" ")[1])
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Neds()
    scrape_obj.write_to_csv()
