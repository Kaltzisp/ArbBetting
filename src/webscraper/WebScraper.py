from abc import abstractmethod
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class WebScraper():
    def __init__(self, driver=None):
        self.source = self.__class__.__name__
        self.odds = []
        self.teams = []
        self.data = []
        if driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=400,1080")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.implicitly_wait(10)
        self.driver = driver

    def game(self, x, game_dict):
        sorted_teams = sorted([x["Team 1"], x["Team 2"]])
        game_string = f'{sorted_teams[0]} vs {sorted_teams[1]}'
        if game_string not in game_dict:
            game_dict[game_string] = 0
        game_dict[game_string] += 1
        return(f'{sorted_teams[0]} vs {sorted_teams[1]} {game_dict[game_string]}')

    @abstractmethod
    def scrape_data(self):
        pass

    def write_to_csv(self):
        self.scrape_data()
        assert(len(self.data) % 2 == 0)
        data_df = pd.DataFrame({"Team 1": [sorted(self.data[i:i + 2])[0][0] for i in range(0, len(self.data), 2)],
                                "Team 2": [sorted(self.data[i:i + 2])[1][0] for i in range(0, len(self.data), 2)],
                                "Odds 1": [sorted(self.data[i:i + 2])[0][1] for i in range(0, len(self.data), 2)],
                                "Odds 2": [sorted(self.data[i:i + 2])[1][1] for i in range(0, len(self.data), 2)]})

        data_df["Source"] = self.source

        data_df["Time"] = pd.to_datetime('now').tz_localize('Australia/Sydney')
        data_df.drop_duplicates(inplace=True)

        game_dict = {}
        data_df["Game"] = data_df.apply(lambda x: self.game(x, game_dict), axis=1)
        data_df.to_csv(f"src/webscraper/data/{self.source}.csv", index=None)
