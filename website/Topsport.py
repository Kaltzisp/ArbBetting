from website.webscraper import WebScraper
from selenium.webdriver.common.by import By
import re

class Topsport(WebScraper):
    def __init__(self, local):
        super().__init__(local)
        self.source = "Topsport"

    def scrape_data(self):
        link = "https://www.topsport.com.au/Sport/Esports/League_of_Legends_-_Worlds_2022/Matches"
        self.driver.get(link)
        odds = [float(i) for i in re.findall('''<div>(\d+\.\d+)<\/div>''', self.driver.page_source)][:4]
        
        teams = [i for i in re.findall('''\\t([\w\. \d]+)\\n''', self.driver.page_source) if i != 'else'][:len(odds)]
        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = Topsport(True)
    scrape_obj.write_to_csv()
