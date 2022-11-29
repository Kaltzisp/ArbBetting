from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Topsport(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"betlink oddsColumn(?:.|\n)*?<a data-hash=.*?button\">{TEAM_ODDS}<\/a>")]

    def get_teams(self):
        return self.find(rf"<span>{TEAM_NAME} <\/span>")

    def scrape_data(self):
        self.scrape("https://www.topsport.com.au/Sport/Basketball/NBA_Matches/Matches")


if __name__ == "__main__":
    scrape_obj = Topsport()
    scrape_obj.write_to_csv()
