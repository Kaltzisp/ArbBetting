# Imports.
import os
import pandas as pd


def combine_odds():
    # Reading csv files into odds_data.
    data_dir = os.path.join("src", "webscraper", "data")
    odds_data = {}
    csv_paths = os.listdir(data_dir)
    for i, filename in enumerate(csv_paths):
        source = os.path.splitext(filename)[0]
        odds_data[source] = pd.read_csv(os.path.join(data_dir, filename))

    # Creating combined odds data frame.
    odds_df = pd.DataFrame()
    for source_1 in odds_data:
        for source_2 in odds_data:
            df = odds_data[source_1]
            df_1 = df[["Game", "Team 1", "Team 2", "Source", "Odds 1", "Time"]]
            df = odds_data[source_2]
            df_2 = df[["Game", "Team 1", "Team 2", "Source", "Odds 2", "Time"]]
            cross = df_1.merge(df_2, how="outer", on=["Game", "Team 1", "Team 2"])
            odds_df = pd.concat([odds_df, cross])
            odds_df.dropna(inplace=True)

    odds_df = odds_df.rename(columns={
        "Source_x": "Source 1",
        "Source_y": "Source 2",
        "Time_x": "Time 1",
        "Time_y": "Time 2",
    })

    # Calculating % arbitrage.
    odds_df["Arbitrage %"] = 100 * ((odds_df["Odds 1"] * odds_df["Odds 2"]) / (odds_df["Odds 1"] + odds_df["Odds 2"]) - 1)

    # Saving odds.
    odds_df.sort_values(by="Arbitrage %", ascending=False, inplace=True)
    odds_df.to_csv("df_comb.csv", index=False)

    # Saving arbs.
    arb_df = odds_df[odds_df["Arbitrage %"] > 0]
    arb_df.to_csv("df_arb.csv", index=False)


if __name__ == "__main__":
    combine_odds()
