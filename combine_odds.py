import pandas as pd
import numpy as np
import os
from sportsbet import Sportsbet
from ladbrokes import Ladbrokes
from picklebet import Picklebet
from unibet import Unibet
from neds import Neds

scrape_obj = Sportsbet()
scrape_obj.write_to_csv()

scrape_obj = Ladbrokes()
scrape_obj.write_to_csv()

scrape_obj = Picklebet()
scrape_obj.write_to_csv()

scrape_obj = Unibet()
scrape_obj.write_to_csv()

scrape_obj = Neds()
scrape_obj.write_to_csv()

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