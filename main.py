from src.webscraper import total_odds
from src.arb import arb
from src.bonus import bonus
from src.mug import mug

if __name__ == "__main__":
    total_odds.main()
    arb.main()
    bonus.main(bonus_amount=100, bonus_source="Betright")
    mug.main()
