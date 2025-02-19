from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Unibet(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"Matches / Odds are not available at the moment"

    def get_odds(self):
        return [float(i) for i in self.find(rf"betButtonDisplay\"><div class=\"_20570\">.*?\"_278bc\".*?{TEAM_ODDS}<\/span>")]

    def get_teams(self):
        return self.find(rf"isExpandedView.*?teamName\">{TEAM_NAME}<")

    def scrape_data(self):
        self.scrape("https://www.unibet.com.au/betting/sports/filter/basketball/nba/all/matches")
        self.scrape("https://www.unibet.com.au/betting/sports/filter/american_football/nfl/all/matches")
        self.scrape("https://www.unibet.com.au/betting/sports/filter/ufc_mma/ufc/all/matches", name_index=0)


if __name__ == "__main__":
    scrape_obj = Unibet()
    scrape_obj.write_to_csv()
