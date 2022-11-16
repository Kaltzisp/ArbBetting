from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Elitebet(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"<span>{TEAM_ODDS}<\/span>")]

    def get_teams(self):
        return self.find(rf"css-1pex9yp\">{TEAM_NAME}<\/p>")

    def scrape_data(self):
        self.scrape("https://www.elitebet.com.au/sports/Basketball/NBA/BASK")
        self.scrape("https://www.elitebet.com.au/sports/Mixed_Martial_Arts/MMA", name_index=-1)


if __name__ == "__main__":
    scrape_obj = Elitebet()
    scrape_obj.write_to_csv()
