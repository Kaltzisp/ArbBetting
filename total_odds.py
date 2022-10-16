import pandas as pd
import numpy as np
import os
from os.path import dirname, basename, isfile, join
import glob
import datetime
import traceback
import logging
import math
import time

logging.basicConfig(filename=f'logs/{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log', encoding='utf-8', level=logging.INFO)

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        local = bool(sys.argv[1])
    else:
        local = True

    hedge_source = "Sportsbet"
    hedge_amount = 0
    hedge_bonus = 100

    modules = glob.glob(join(dirname(__file__) + '''\\website''', "*.py"))
    website_list = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
    for website in website_list:
        start = time.time()
        if website != 'webscraper':
            exec(f"from website.{website} import {website}")
            exec(f"scrape_obj = {website}({local})")
            try:
                logging.info(f"Scraping data from {website}")
                scrape_obj.write_to_csv()
                logging.info(f"Succesfully scraped from {website}")
            except Exception as e:
                logging.info(f"Crash scraping data from {website}")
                logging.info(traceback.format_exc())
            logging.info(f"{website} finished in {time.time() - start} seconds")

    file_list = os.listdir('data/')
    source_list = [file[:-4] for file in file_list]
    data_dict = {}

    for i, file in enumerate(file_list):
        file_df = pd.read_csv(f'data/{file}')
        file_df['Source 1'] = file_df['Source']
        file_df['Source 2'] = file_df['Source']
        data_dict[file[:-4]] = file_df

    total_df = pd.DataFrame()
    for source_1 in data_dict:
        for source_2 in data_dict:
            df_1 = data_dict[source_1][['Team 1', 'Team 2', 'Odds 1', 'Game', 'Source 1']].copy()
            df_2 = data_dict[source_2][['Team 1', 'Team 2', 'Odds 2', 'Game', 'Source 2']].copy()
            total_df = total_df.append(df_1.merge(df_2, how="left", on=['Team 1', 'Team 2', 'Game']))
    total_df.dropna(inplace=True)

    total_df["Arbitrage %"] = 100*(total_df["Odds 1"] * total_df["Odds 2"])/(total_df["Odds 1"] + total_df["Odds 2"]) - 100
    total_df["Implied Probability"] = 1/total_df["Odds 1"] + 1/total_df["Odds 2"]

    total_df.to_csv("comb.csv", index=False)

    opp_df = total_df[total_df["Implied Probability"] < 1]
    arb_df = pd.DataFrame()

    for i in range(len(opp_df)):
        row = opp_df.iloc[i]
        for j in range(3):
            sub_row = row[["Team 1", "Team 2", "Odds 1", "Odds 2", "Source 1", "Source 2", "Game", "Implied Probability"]].copy()
            if j == 0:
                amount_1 = round(sub_row["Odds 2"]*100)
                amount_2 = round(sub_row["Odds 1"]*100)
            elif j == 1:
                amount_1 = 100
                amount_2 = round((sub_row["Odds 1"]-1)*100)
            elif j == 2:
                amount_1 = round((sub_row["Odds 2"]-1)*100)
                amount_2 = 100
            factor = math.gcd(amount_1, amount_2)
            sub_row["Amount 1"] = amount_1//factor
            sub_row["Amount 2"] = amount_2//factor
            sub_row["Amount 1 Min"] = 1/sub_row["Odds 1"]
            sub_row["Amount 1 Max"] = 1 - (1/sub_row["Odds 2"])
            sub_row["Amount 2 Min"] = 1/sub_row["Odds 2"]
            sub_row["Amount 2 Max"] = 1 - (1/sub_row["Odds 1"])
            arb_df = arb_df.append(sub_row)

    if len(arb_df) > 0: 
        arb_df["Team 1 Win Return %"] = 100*((arb_df["Odds 1"] * arb_df["Amount 1"]) / (arb_df["Amount 1"] + arb_df["Amount 2"]) - 1)
        arb_df["Team 2 Win Return %"] = 100*((arb_df["Odds 2"] * arb_df["Amount 2"]) / (arb_df["Amount 1"] + arb_df["Amount 2"]) - 1)
        arb_df.sort_values(by="Implied Probability", inplace=True)
    arb_df.to_csv("arb.csv", index=False)

    opp_df = total_df[((total_df["Source 1"] == hedge_source) | (total_df["Source 2"] == hedge_source)) & (total_df["Source 1"] != total_df["Source 2"])].copy()
    hedge_df = pd.DataFrame()
    for i in range(2):
        sub_df = opp_df[opp_df[f"Source {i + 1}"] == hedge_source].copy()
        sub_df["Hedge Amount"] = ((sub_df[f"Odds {i+1}"] - 1)*hedge_bonus + sub_df[f"Odds {i+1}"] * hedge_amount)/ sub_df[f"Odds {(i+3)%2+1}"]
        sub_df["Payout"] = sub_df[f"Odds {i + 1}"] * hedge_amount + (sub_df[f"Odds {i+1}"] - 1) * hedge_bonus - sub_df["Hedge Amount"] - hedge_amount
        hedge_df = hedge_df.append(sub_df)
    hedge_df.sort_values(by="Payout", ascending=False, inplace=True)
    hedge_df.to_csv("hedge.csv", index=False)
