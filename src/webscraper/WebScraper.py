import re
import time
from abc import abstractmethod
import pandas as pd
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from src.core.utils import log, TEAM_MAPPING
import numpy as np


class WebScraper():
    def __init__(self, driver, hidden):
        self.source = self.__class__.__name__
        self.data_dict = {'Team 1': [], 'Team 2': [], 'Odds 1': [], 'Odds 2': [], 'Link': []}
        self.total_odds = []
        self.total_teams = []
        if driver is None:
            driver_options = webdriver.ChromeOptions()
            if hidden:
                driver_options.add_argument("--headless")
                log.info(f"{self.source}: Running WebScraper...")
            else:
                driver_options.add_argument("--window-size=400,1080")
            driver_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            driver_options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
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
    def await_odds(self, timein, timeout):
        time.sleep(timein)
        odds = self.get_odds()
        while len(odds) == 0 and timeout > 0 and not self.find(self.no_markets):
            timeout -= 0.5
            time.sleep(0.5)
            odds = self.get_odds()
        return odds

    # Scrape function using get_odds and get_teams.
    def scrape(self, url, name_index=None, timein=0.5, timeout=5, silent=False):
        self.driver.get(url)
        odds = self.await_odds(timein, timeout)
        teams = self.get_teams()
        if name_index is not None:
            teams = [team.split(" ")[name_index] for team in teams]
            teams = [re.sub(",", "", team) for team in teams]
        if len(odds) == 0 and not silent:
            log.error(f"{self.source}: No odds found.\n{url}")
        elif len(odds) != len(teams):
            log.error(f"{self.source}: Scraping failed.\n{url}")
        elif len(odds) % 2 != 0:
            log.error(f"{self.source}: Uneven number of odds.\n{url}")
        else:
            self.total_odds += odds
            self.total_teams += teams
            self.data_dict['Link'] += [url] * (len(odds) // 2)

    def scrape_all(self, comps_url, url, name_index=None, timein=0, timeout=5):
        self.driver.get(comps_url)
        competitions = self.get_comps()
        while len(competitions) == 0 and timeout > 0:
            timeout -= 0.5
            time.sleep(0.5)
            competitions = self.get_comps()
        for comp in competitions:
            comp = url.replace("%URL%", comp)
            self.scrape(comp, name_index, timein, timeout, silent=True)

    # Write odds to csv file.
    def write_to_csv(self):
        self.scrape_data()

        self.data_dict["Team 1"] += self.total_teams[::2]
        self.data_dict["Team 2"] += self.total_teams[1::2]
        self.data_dict["Odds 1"] += self.total_odds[::2]
        self.data_dict["Odds 2"] += self.total_odds[1::2]
        data_df = pd.DataFrame(self.data_dict)

        data_df["Team 1"] = data_df["Team 1"].replace(TEAM_MAPPING)
        data_df["Team 2"] = data_df["Team 2"].replace(TEAM_MAPPING)

        data_df["Team 1 Temp"] = data_df[["Team 1", "Team 2"]].min(axis=1)
        data_df["Team 2 Temp"] = data_df[["Team 1", "Team 2"]].max(axis=1)
        data_df["Odds 1 Temp"] = np.where(data_df["Team 1 Temp"] == data_df["Team 1"], data_df["Odds 1"], data_df["Odds 2"])
        data_df["Odds 2 Temp"] = np.where(data_df["Team 2 Temp"] == data_df["Team 2"], data_df["Odds 2"], data_df["Odds 1"])
        data_df["Team 1"] = data_df["Team 1 Temp"]
        data_df["Team 2"] = data_df["Team 2 Temp"]
        data_df["Odds 1"] = data_df["Odds 1 Temp"]
        data_df["Odds 2"] = data_df["Odds 2 Temp"]
        data_df.drop(columns=["Team 1 Temp", "Team 2 Temp", "Odds 1 Temp", "Odds 2 Temp"], inplace=True)

        data_df["Source"] = self.source

        data_df["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_df.drop_duplicates(inplace=True)

        game_dict = {}
        data_df["Game"] = data_df.apply(lambda x: self.game(x, game_dict), axis=1)
        data_df.to_csv(f"src/webscraper/data/{self.source}.csv", index=None)
