import pandas as pd
from os import listdir, path, mkdir
from shutil import rmtree
import numpy as np
from src.horse.scrape_odds import scrape_odds

def main():
    pass

if __name__ == "__main__":
    scrape_odds()

    # Clearing data files
    if path.isdir('src/horse/result'):
        rmtree('src/horse/result')
    mkdir('src/horse/result')

    betfairlay_df = pd.read_csv("src/horse/data/Betfairlay.csv")
    betfairlay_df["Win Probability"] = 1/betfairlay_df["Odds"]
    betfairlaytop3_df = pd.read_csv("src/horse/data/BetfairlayTop3.csv")
    betfairlaytop3_df["Top 3 Probability"] = 1/betfairlaytop3_df["Odds"]
    betfair_df = betfairlay_df[["Horse", "Win Probability"]].merge(betfairlaytop3_df[["Horse", "Top 3 Probability"]], how="outer", on="Horse")
    betfair_df["Top 3 Probability"] = np.maximum(betfair_df["Top 3 Probability"], betfair_df["Win Probability"])
    for fname in listdir('src/horse/data'):
        if "Betfair" not in fname:
            source_df = pd.read_csv('src/horse/data/' + fname)
            source_df = source_df.merge(betfair_df, on="Horse")
            source_df["EV"] = 50*source_df["Odds"]*source_df["Win Probability"] + (source_df["Win Probability"] - source_df["Top 3 Probability"])*30 - 50
            source_df.to_csv(f"src/horse/result/{fname}", index=False)
