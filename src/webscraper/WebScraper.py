import re
import time
import logging
from abc import abstractmethod
import pandas as pd
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class WebScraper():
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

    @abstractmethod
    def scrape_data(self):
        pass

    # Get match data.
    def game(self, x, game_dict):
        sorted_teams = sorted([x["Team 1"], x["Team 2"]])
        game_string = f'{sorted_teams[0]} vs {sorted_teams[1]}'
        if game_string not in game_dict:
            game_dict[game_string] = 0
        game_dict[game_string] += 1
        return(f'{sorted_teams[0]} vs {sorted_teams[1]} {game_dict[game_string]}')

    # Performs a regex search on the web driver html.
    def find(self, pattern):
        return re.findall(pattern, self.driver.page_source)

    # Sleeps web driver until odds are loaded, or until no_market message is found.
    def await_odds(self, timeout):
        while timeout > 0:
            odds = self.get_odds()
            time.sleep(0.5)
            timeout -= 0.5
            if odds:
                break
            if self.find(self.no_markets):
                time.sleep(0.5)
                odds = self.get_odds()
                # break
        return odds

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
            assert len(odds) % 2 == 0, "Uneven odds/teams"
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
        data_df = pd.DataFrame({"Team 1": [sorted(self.data[i:i + 2])[0][0] for i in range(0, len(self.data), 2)],
                                "Team 2": [sorted(self.data[i:i + 2])[1][0] for i in range(0, len(self.data), 2)],
                                "Odds 1": [sorted(self.data[i:i + 2])[0][1] for i in range(0, len(self.data), 2)],
                                "Odds 2": [sorted(self.data[i:i + 2])[1][1] for i in range(0, len(self.data), 2)]})

        data_df["Source"] = self.source

        data_df["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_df.drop_duplicates(inplace=True)

        game_dict = {}
        data_df["Game"] = data_df.apply(lambda x: self.game(x, game_dict), axis=1)
        data_df.to_csv(f"src/webscraper/data/{self.source}.csv", index=None)
