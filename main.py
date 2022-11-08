from src.arb import arb
from src.bonus import bonus
from src.mug import mug
from src.core.scrape_odds import scrape_odds
from src.core.combine_odds import combine_odds

if __name__ == "__main__":
    scrape_odds()
    combine_odds()
    arb.main()
    bonus.main(bonus_amount=100, bonus_source="Betright")
    mug.main()
