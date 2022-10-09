from abc import abstractmethod
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class WebScraper():
    def __init__(self, local):
        self.source = None
        self.odds = []
        self.teams = []
        self.data = []
        if local:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            self.driver.implicitly_wait(10)
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')        #remove this for easy debbuing on your laptop /pc
            chrome_options.add_argument('--no-sandbox')                             
            chrome_options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome('chromedriver',options=chrome_options)
            self.driver.implicitly_wait(10)

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
        data_df = pd.DataFrame({"Team 1": [sorted(self.data[i:i+2])[0][0] for i in range(0, len(self.data), 2)],
                                "Team 2": [sorted(self.data[i:i+2])[1][0] for i in range(0, len(self.data), 2)],
                                "Odds 1": [sorted(self.data[i:i+2])[0][1] for i in range(0, len(self.data), 2)],
                                "Odds 2": [sorted(self.data[i:i+2])[1][1] for i in range(0, len(self.data), 2)]})

        data_df["Source"] = self.source

        game_dict = {}
        data_df["Game"] = data_df.apply(lambda x: self.game(x, game_dict), axis=1)
        data_df["Time"] = pd.to_datetime('now').tz_localize('Australia/Sydney')
        data_df.drop_duplicates(inplace=True)

        data_df.to_csv(f"data/{self.source}.csv", index=None)
        self.driver.close()
