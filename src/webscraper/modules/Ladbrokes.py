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
        self.scrape("https://www.ladbrokes.com.au/sports/mma/ufc-281-adesanya-vs-pereira", name_index=-1)
        self.scrape("https://www.ladbrokes.com.au/sports/mma/ufc-fight-night-spivak-vs-lewis", name_index=-1)
        self.scrape("https://www.ladbrokes.com.au/sports/mma/ufc-282-teixeira-vs-prochazka", name_index=-1)
        self.scrape("https://www.ladbrokes.com.au/sports/basketball/usa/nba")
        self.scrape("https://www.ladbrokes.com.au/sports/tennis/bratislava-challenger", name_index=-1)
        self.scrape("https://www.ladbrokes.com.au/sports/tennis/roanne-challenger", name_index=-1)
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Ladbrokes()
    scrape_obj.write_to_csv()
