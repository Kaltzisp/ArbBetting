from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Betright(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"<span class=\"place-bet__odds ng-binding\">{TEAM_ODDS}<\/span>")]

    def get_teams(self):
        return self.find(rf"headline-wrap ng-binding\">{TEAM_NAME}<\/div>")

    def scrape_data(self):
        self.scrape("https://www.betright.com.au/sports/Martial-Arts/128", name_index=-1)
        self.scrape("https://www.betright.com.au/sports/Basketball/United-States-of-America/NBA/54")
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Betright()
    scrape_obj.write_to_csv()
