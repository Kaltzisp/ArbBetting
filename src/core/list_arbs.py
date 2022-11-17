# Imports.
import math
import pandas as pd


def main(short=False):
    total_df = pd.read_csv("table_comb.csv")

    if short:
        arb_df = total_df[total_df["Arbitrage %"] > 0]
        arb_df = arb_df[["Source 1", "Team 1", "Odds 1", "Source 2", "Team 2", "Odds 2", "Link 1", "Link 2", "Arbitrage %"]]
        arb_df.to_csv("table_arb.csv", index=False)
    else:
        opp_df = total_df[total_df["Implied Probability"] < 1]
        arb_df = pd.DataFrame()

        for i in range(len(opp_df)):
            row = opp_df.iloc[i]
            for j in range(3):
                sub_row = row[["Team 1", "Team 2", "Odds 1", "Odds 2", "Source 1", "Source 2", "Link 1", "Link 2", "Time 1", "Time 2", "Game", "Implied Probability"]].copy()
                if j == 0:
                    amount_1 = round(sub_row["Odds 2"] * 100)
                    amount_2 = round(sub_row["Odds 1"] * 100)
                elif j == 1:
                    amount_1 = 100
                    amount_2 = round((sub_row["Odds 1"] - 1) * 100)
                elif j == 2:
                    amount_1 = round((sub_row["Odds 2"] - 1) * 100)
                    amount_2 = 100
                factor = math.gcd(amount_1, amount_2)
                sub_row["Amount 1"] = amount_1 // factor
                sub_row["Amount 2"] = amount_2 // factor
                sub_row["Amount 1 Min"] = 1 / sub_row["Odds 1"]
                sub_row["Amount 1 Max"] = 1 - (1 / sub_row["Odds 2"])
                sub_row["Amount 2 Min"] = 1 / sub_row["Odds 2"]
                sub_row["Amount 2 Max"] = 1 - (1 / sub_row["Odds 1"])
                arb_df = arb_df.append(sub_row)

        if len(arb_df) > 0:
            arb_df["Team 1 Win Return %"] = 100 * ((arb_df["Odds 1"] * arb_df["Amount 1"]) / (arb_df["Amount 1"] + arb_df["Amount 2"]) - 1)
            arb_df["Team 2 Win Return %"] = 100 * ((arb_df["Odds 2"] * arb_df["Amount 2"]) / (arb_df["Amount 1"] + arb_df["Amount 2"]) - 1)
            arb_df.sort_values(by="Implied Probability", inplace=True)
        arb_df.to_csv("table_arb.csv", index=False)


if __name__ == "__main__":
    main()
