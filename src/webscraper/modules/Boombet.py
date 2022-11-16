from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Boombet(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"<span class=\"oddsValue d-block d-md-flex\">{TEAM_ODDS}<\/span>")]

    def get_teams(self):
        return self.find(rf"<span class=\"teamName d-block d-md-flex pb-1\">{TEAM_NAME}<\/span>")

    def scrape_data(self):
        self.scrape("https://www.boombet.com.au/sport-menu/Sport/Mixed%20Martial%20Arts/UFC", name_index=-1)
        self.scrape("https://www.boombet.com.au/sport-menu/Sport/Basketball/US%20NBA%20Regular%20Season-22")


if __name__ == "__main__":
    scrape_obj = Boombet()
    scrape_obj.write_to_csv()
