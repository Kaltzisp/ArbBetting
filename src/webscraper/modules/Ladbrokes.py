from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Ladbrokes(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"<span data-testid=\"price-button-odds\" has-boost=\"true\">{TEAM_ODDS}<\/span>")]

    def get_teams(self):
        return self.find(rf"<span class=\"displayTitle\">{TEAM_NAME}<\/span>")

    def scrape_data(self):
        self.scrape("https://www.ladbrokes.com.au/sports/basketball/usa/nba")
        self.scrape("https://www.ladbrokes.com.au/sports/ice-hockey/usa/nhl")


if __name__ == "__main__":
    scrape_obj = Ladbrokes()
    scrape_obj.write_to_csv()
