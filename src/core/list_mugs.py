import pandas as pd
import numpy as np


def main(mug_source="Betrmug", mug_amount=100):
    total_df = pd.read_csv("table_comb.csv")

    game_dict = {}

    opp_df = total_df[((total_df["Source 1"] == mug_source) | (total_df["Source 2"] == mug_source)) &
                      ((total_df["Source 1"].str.contains("Betfair")) ^ (total_df["Source 2"].str.contains("Betfair"))) &
                      (total_df["Source 1"] != total_df["Source 2"])].copy()

    uncomb_df = total_df[total_df["Source 1"] == total_df["Source 2"]]
    for game in uncomb_df["Game"].unique():
        game_df = uncomb_df[uncomb_df["Game"] == game].copy()
        game_df["Value 1"] = game_df["Odds 1"] / max(game_df["Odds 1"])
        game_df["Value 2"] = game_df["Odds 2"] / max(game_df["Odds 2"])
        for i in range(len(game_df)):
            row = game_df.iloc[i]
            game_dict[(row["Source 1"], row["Team 1"])] = row["Value 1"]
            game_dict[(row["Source 2"], row["Team 2"])] = row["Value 2"]

    mug_df = pd.DataFrame()
    for i in range(2):
        sub_df = opp_df[opp_df[f"Source {i + 1}"] == mug_source].copy()
        sub_df["Amount"] = (sub_df[f"Odds {i+1}"] * mug_amount) / sub_df[f"Odds {(i+3)%2+1}"]
        sub_df["Payout"] = sub_df[f"Odds {i + 1}"] * mug_amount - sub_df["Amount"] - mug_amount
        mug_df = mug_df.append(sub_df)

    def get_value(x):
        if x["Source 1"] == mug_source:
            return(game_dict[(x["Source 1"], x["Team 1"])])
        elif x["Source 2"] == mug_source:
            return(game_dict[(x["Source 2"], x["Team 2"])])
        else:
            return(np.nan)

    mug_df["Value"] = mug_df.apply(lambda x: get_value(x), axis=1)
    mug_df.sort_values(by="Payout", ascending=False, inplace=True)
    mug_df.to_csv("mug.csv", index=False)


if __name__ == "__main__":
    main()
