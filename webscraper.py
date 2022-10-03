import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebScraper():
    def __init__(self):
        self.source = None
        self.odds = []
        self.teams = []
        self.data = []
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
        self.driver.implicitly_wait(10)

    def game(self, x):
        sorted_teams = sorted([x["Team 1"], x["Team 2"]])
        return(f'{sorted_teams[0]} vs {sorted_teams[1]}')

    def scrape_data(self):
        pass

    def write_to_csv(self):
        self.scrape_data()
        data_df = pd.DataFrame({"Team 1": [sorted(self.data[i:i+2])[0][0] for i in range(0, len(self.data), 2)],
                                "Team 2": [sorted(self.data[i:i+2])[1][0] for i in range(0, len(self.data), 2)],
                                "Odds 1": [sorted(self.data[i:i+2])[0][1] for i in range(0, len(self.data), 2)],
                                "Odds 2": [sorted(self.data[i:i+2])[1][1] for i in range(0, len(self.data), 2)]})

        data_df["Source"] = self.source
        data_df["Game"] = data_df.apply(lambda x: self.game(x), axis=1)
        data_df["Time"] = pd.to_datetime('now').tz_localize('Australia/Sydney')
        data_df.to_csv(f"data/{self.source}.csv", index=None)
        self.driver.close()
