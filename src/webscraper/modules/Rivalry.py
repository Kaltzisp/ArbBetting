from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Rivalry(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"outcome-name(?:(?!specifier).)*?<div class=\"outcome-odds\">[\s\"]+{TEAM_ODDS}[\s\"]+")]

    def get_teams(self):
        return self.find(rf"<div class=\"outcome-name\">{TEAM_NAME}<\/div>")

    def scrape_data(self):
        self.scrape("https://www.rivalry.com/au/sports/mma-betting", name_index=-1)
        self.scrape("https://www.rivalry.com/au/sports/basketball-betting/3378-nba")


if __name__ == "__main__":
    scrape_obj = Rivalry()
    scrape_obj.write_to_csv()
