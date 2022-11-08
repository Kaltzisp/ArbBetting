import pandas as pd
from selenium.webdriver.common.by import By


def main(bonus_source="Tab", bonus_amount=25):
    total_df = pd.read_csv("comb.csv")

    opp_df = total_df[((total_df["Source 1"] == bonus_source) | (total_df["Source 2"] == bonus_source)) & (total_df["Source 1"] != total_df["Source 2"])].copy()
    bonus_df = pd.DataFrame()
    for i in range(2):
        sub_df = opp_df[opp_df[f"Source {i + 1}"] == bonus_source].copy()
        sub_df["Amount"] = ((sub_df[f"Odds {i+1}"] - 1) * bonus_amount) / sub_df[f"Odds {(i+3)%2+1}"]
        sub_df["Payout"] = (sub_df[f"Odds {i+1}"] - 1) * bonus_amount - sub_df["Amount"]
        bonus_df = bonus_df.append(sub_df)
    bonus_df.sort_values(by="Payout", ascending=False, inplace=True)
    bonus_df.to_csv("bonus.csv", index=False)


if __name__ == "__main__":
    main()
