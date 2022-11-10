from src.core.scrape_odds import scrape_odds
from src.core.combine_odds import combine_odds
from src.core import list_arbs, list_bonuses, list_mugs


if __name__ == "__main__":
    scrape_odds(hidden=True)
    combine_odds()
    list_arbs.main()
    list_bonuses.main(bonus_source="Bluebet", bonus_amount=100)
    list_mugs.main(mug_source="Betr", mug_amount=100)
