import pandas as pd
import numpy as np
import os
from os.path import dirname, basename, isfile, join
import glob
import logging
import datetime

logger = logging.getLogger(__name__)
f_handler = logging.FileHandler(f'logs/{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(f_handler)

modules = glob.glob(join(dirname(__file__) + '''\\website''', "*.py"))
website_list = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
for website in website_list:
    if website != 'webscraper':
        exec(f"from website.{website} import {website}")
        exec(f"scrape_obj = {website}()")
        try:
            scrape_obj.write_to_csv()
        except Exception as e:
            print(website, e)

file_list = os.listdir('data/')
source_list = [file[:-4] for file in file_list]

comb_df = pd.DataFrame()
for i, file in enumerate(file_list):
    file_df = pd.read_csv(f'data/{file}')
    if i == 0:
        comb_df = file_df
    elif i == 1:
        comb_df = comb_df.merge(file_df, how="outer", on=["Team 1", "Team 2", "Game"], suffixes=(" " + comb_df["Source"].unique()[0], " " + file[:-4]))
    else:
        file_df.columns = file_df.columns.map(lambda x: str(x) + f' {file[:-4]}' if (x not in ["Team 1", "Team 2", "Game"]) else x)
        comb_df = comb_df.merge(file_df, how="outer", on=["Team 1", "Team 2", "Game"])

for source in source_list:
    comb_df[f"Odds 1 {source}"] = comb_df[f"Odds 1 {source}"].fillna(0)
    comb_df[f"Odds 2 {source}"] = comb_df[f"Odds 2 {source}"].fillna(0)

comb_df["Odds 1"] = np.maximum.reduce([comb_df[f"Odds 1 {source}"] for source in source_list])
comb_df["Odds 2"] = np.maximum.reduce([comb_df[f"Odds 2 {source}"] for source in source_list])
comb_df["Odds 1 Source"] = np.nan
comb_df["Odds 2 Source"] = np.nan
for source in source_list:
    comb_df.loc[comb_df['Odds 1'] == comb_df[f'Odds 1 {source}'], 'Odds 1 Source'] = source
    comb_df.loc[comb_df['Odds 2'] == comb_df[f'Odds 2 {source}'], 'Odds 2 Source'] = source

comb_df = comb_df[["Team 1", "Team 2", "Odds 1", "Odds 2", "Odds 1 Source", "Odds 2 Source", "Game"]]

comb_df["Arbitrage %"] = 100*(comb_df["Odds 1"] * comb_df["Odds 2"])/(comb_df["Odds 1"] + comb_df["Odds 2"]) - 100
comb_df["Implied Probability"] = 1/comb_df["Odds 1"] + 1/comb_df["Odds 2"]

comb_df.to_csv("comb.csv", index=False)

opp_df = comb_df[comb_df["Implied Probability"] < 1]
arb_df = pd.DataFrame()

for i in range(len(opp_df)):
    row = opp_df.iloc[i]
    for j in range(3):
        sub_row = row[["Team 1", "Team 2", "Odds 1", "Odds 2", "Odds 1 Source", "Odds 2 Source", "Game"]].copy()
        if j == 0:
            sub_row["Amount 1"] = sub_row["Odds 2"]
            sub_row["Amount 2"] = sub_row["Odds 1"]
        elif j == 1:
            sub_row["Amount 1"] = 1
            sub_row["Amount 2"] = sub_row["Odds 1"]-1
        elif j == 2:
            sub_row["Amount 1"] = sub_row["Odds 2"]-1
            sub_row["Amount 2"] = 1
        arb_df = arb_df.append(sub_row)

if len(arb_df) > 0:
    arb_df["Team 1 Win Return %"] = 100*((arb_df["Odds 1"] * arb_df["Amount 1"]) / (arb_df["Amount 1"] + arb_df["Amount 2"]) - 1)
    arb_df["Team 2 Win Return %"] = 100*((arb_df["Odds 2"] * arb_df["Amount 2"]) / (arb_df["Amount 1"] + arb_df["Amount 2"]) - 1)

    arb_df.to_csv("arb.csv", index=False)
