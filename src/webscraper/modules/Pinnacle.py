from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Pinnacle(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"There are currently no active markets."

    def get_odds(self):
        return [float(i) for i in self.find(rf"style_price__[\w]+\">{TEAM_ODDS}<\/span>")]

    def get_teams(self):
        return self.find(rf"ellipsis event-row-participant style_participant__[\w-]+\">{TEAM_NAME}<\/span>")

    def scrape_data(self):
        self.scrape("https://www.pinnacle.com/en/basketball/nba/matchups/#period:0:moneyline")
        

if __name__ == "__main__":
    scrape_obj = Pinnacle()
    scrape_obj.write_to_csv()
