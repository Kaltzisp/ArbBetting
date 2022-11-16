from src.horse.HorseWebScraper import HorseWebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Betfairlay(HorseWebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"There are no events to be displayed"

    def get_odds(self):
        odds = [float(i) for i in self.find(rf"<span class=\"bet-button-price\">{TEAM_ODDS}<\/span>")]
        for i, odd in enumerate(odds):
            if odd == 0:
                odds[i] = 1000
        odds = odds[3::6]
        return odds

    def get_teams(self):
        return self.find(rf"modal\">{TEAM_NAME}<")[:len(self.get_odds())]

    def scrape_data(self):
        self.scrape("https://www.betfair.com.au/exchange/plus/horse-racing/market/1.206304769")


if __name__ == "__main__":
    scrape_obj = Betfairlay()
    scrape_obj.write_to_csv()
