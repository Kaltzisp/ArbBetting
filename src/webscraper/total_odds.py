# Imports.
import os
import time
import logging
import datetime
import pandas as pd
from src import utils

now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
logging.basicConfig(filename=f'src/webscraper/logs/{now}.log', encoding='utf-8', level=logging.INFO)


def main():
    # Setting selenium driver.
    driver = None

    # options = webdriver.ChromeOptions()
    # options.add_argument("--window-size=400,1080")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # driver.implicitly_wait(10)

    # Running webscraper modules.
    modules = utils.load_modules()
    for module in modules:
        start = time.time()
        scrape_obj = module(driver)
        try:
            logging.info(f"{module.__name__}: Attempting webscrape")
            scrape_obj.write_to_csv()
            logging.info(f"{module.__name__}: Scraped successfully")
        except Exception as e:
            logging.info(f"{module.__name__}: Scraping failed")
            logging.exception(e)
        logging.info(f"{module.__name__} scraped in {time.time() - start} secs")

    file_list = os.listdir('src/webscraper/data/')
    data_dict = {}

    for i, file in enumerate(file_list):
        file_df = pd.read_csv(f'src/webscraper/data/{file}')
        file_df['Source 1'] = file_df['Source']
        file_df['Source 2'] = file_df['Source']
        file_df['Time 1'] = file_df['Time']
        file_df['Time 2'] = file_df['Time']
        data_dict[file[:-4]] = file_df

    odds_df = pd.DataFrame()
    total_df = pd.DataFrame()
    for source_1 in data_dict:
        for source_2 in data_dict:
            df_1 = data_dict[source_1][['Team 1', 'Team 2', 'Odds 1', 'Source 1', 'Time 1', 'Game']].copy()
            df_2 = data_dict[source_2][['Team 1', 'Team 2', 'Odds 2', 'Source 2', 'Time 2', 'Game']].copy()
            total_df = total_df.append(df_1.merge(df_2, how="left", on=['Team 1', 'Team 2', 'Game']))
    total_df.dropna(inplace=True)

    for source in data_dict:
        odds_df = odds_df.append(data_dict[source])
    odds_df.dropna(inplace=True)
    odds_df.to_csv(f"data/odds_{now}.csv", index=False)

    total_df["Arbitrage %"] = 100 * (total_df["Odds 1"] * total_df["Odds 2"]) / (total_df["Odds 1"] + total_df["Odds 2"]) - 100
    total_df["Implied Probability"] = 1 / total_df["Odds 1"] + 1 / total_df["Odds 2"]
    total_df.sort_values(by='Implied Probability', inplace=True)
    total_df.to_csv("comb.csv", index=False)


if __name__ == "__main__":
    main()
