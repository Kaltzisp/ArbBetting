import pandas as pd
import numpy as np
from itertools import combinations, product

def main(source="Betr", amount=50):
    total_df = pd.read_csv("table_comb.csv")

    opp_df = total_df[((total_df["Source 1"] == source) & (total_df["Source 2"] == source))].copy()
    opp_df["NBA?"] = opp_df["Link 1"].apply(lambda x: 'https://betr.com.au/sportsbook#/sport/13/competition/1000649/1003042' == x)
    opp_df = opp_df[opp_df["NBA?"]].reset_index(drop=True)
    opp_df["Lay 1"] = opp_df["Odds 2"]/(opp_df["Odds 2"] - 1)
    opp_df["Lay 2"] = opp_df["Odds 1"]/(opp_df["Odds 1"] - 1)
    opp_df["Probability 1"] = (1/opp_df["Lay 1"])
    opp_df["Probability 2"] = (1/opp_df["Lay 2"])
    
    games_list = list(combinations([i for i in range(len(opp_df))], 3))
    multi_dict = {"Leg 1": [], "Leg 2": [], "Leg 3": [], "Odds 1": [], "Odds 2": [], "Odds 3": [], "Probability 1": [], "Probability 2": [], "Probability 3": []}
    for games in games_list:
        rows = [opp_df.iloc[i] for i in range(3)]
        for teams in list(product([1, 2], repeat=3)):
            for i, team in enumerate(teams):
                multi_dict[f"Leg {i+1}"].append(rows[i][f"Team {team}"])
                multi_dict[f"Odds {i+1}"].append(rows[i][f"Odds {team}"])
                multi_dict[f"Probability {i+1}"].append(rows[i][f"Probability {team}"])
    multi_df = pd.DataFrame(multi_dict)
    multi_df["Multi Odds"] = multi_df["Odds 1"] * multi_df["Odds 2"] * multi_df["Odds 3"]
    multi_df["Multi Probability"] = multi_df["Probability 1"] * multi_df["Probability 2"] * multi_df["Probability 3"]
    multi_df["One Leg Fail Probability"] = (1-multi_df["Probability 1"]) * multi_df["Probability 2"] * multi_df["Probability 3"] + multi_df["Probability 1"] * (1-multi_df["Probability 2"]) * multi_df["Probability 3"] + multi_df["Probability 1"] * multi_df["Probability 2"] * (1-multi_df["Probability 3"])
    multi_df["EV"] = (multi_df["Multi Probability"] * multi_df["Multi Odds"] + multi_df["One Leg Fail Probability"] * 0.6) * 50 - 50
    multi_df.sort_values(by="EV", ascending=False, inplace=True)
    multi_df.to_csv("table_multi.csv", index=False)


if __name__ == "__main__":
    main()