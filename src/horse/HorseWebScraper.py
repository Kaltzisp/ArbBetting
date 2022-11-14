import re
import time
import logging
from abc import abstractmethod
import pandas as pd
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from src.webscraper.WebScraper import WebScraper

class HorseWebScraper(WebScraper):
    def __init__(self, driver, hidden):
        self.source = self.__class__.__name__
        self.total_odds = []
        self.total_teams = []
        self.odds = []
        self.teams = []
        self.data = []
        if driver is None:
            options = webdriver.ChromeOptions()
            if hidden:
                options.add_argument("--headless")
            else:
                options.add_argument("--window-size=400,1080")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.implicitly_wait(10)
        self.driver = driver

    # Scrape function using get_odds and get_teams.
    def scrape(self, url, name_index=None, timeout=5):
        try:
            self.driver.get(url)
            odds = self.await_odds(timeout)
            teams = self.get_teams()
            if name_index is not None:
                teams = [team.split(" ")[name_index] for team in teams]
            teams = [re.sub(",", "", team) for team in teams]
            assert len(odds) == len(teams), "Scraping encountered errors."
            assert len(odds) > 0, "No odds found"
            self.total_odds += odds
            self.total_teams += teams
        except Exception as e:
            logging.exception(e)
            logging.info(url)
            print("Import failed from " + url)
            print(e)

    # Write odds to csv file.
    def write_to_csv(self):
        self.scrape_data()
        data_df = pd.DataFrame({"Horse": [self.data[i][0] for i in range(0, len(self.data))],
                                "Odds": [self.data[i][1] for i in range(0, len(self.data))]})

        data_df["Source"] = self.source

        data_df["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_df.drop_duplicates(inplace=True)

        data_df.to_csv(f"src/horse/data/{self.source}.csv", index=None)
