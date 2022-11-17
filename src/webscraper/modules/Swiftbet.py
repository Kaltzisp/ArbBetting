from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Swiftbet(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"<h1>N\/A<\/h1>"

    def get_odds(self):
        return [float(i) for i in self.find(rf"transform=\"none\">{TEAM_ODDS}<\/div>")]

    def get_teams(self):
        return self.find(rf"SelectionTitleText-.*?id=\"multiBet\" transform=\"none\">{TEAM_NAME}<\/div>")

    def scrape_data(self):
        self.scrape("https://swiftbet.com.au/sports/basketball/nba-1000015")
        self.scrape("https://swiftbet.com.au/sports/american-football/nfl-1000540")
        self.scrape("https://swiftbet.com.au/sports/boxing/professional-boxing-1000014", name_index=0, timeout=20)


if __name__ == "__main__":
    scrape_obj = Swiftbet()
    scrape_obj.write_to_csv()
