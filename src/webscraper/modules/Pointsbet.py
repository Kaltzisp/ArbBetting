from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Pointsbet(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"There are currently no active markets."

    def get_odds(self):
        return [float(i) for i in self.find(rf"(?:Market0|Outcome[0-9])OddsButton.*?<span class=\"fheif50\">{TEAM_ODDS}<\/span>")]

    def get_teams(self):
        return self.find(rf"(?:<p class=\"feu1e1k fyraa0v f1qmefvr\">|FixedOdds.*?>.*?>){TEAM_NAME}<\/(?:p|span)")

    def scrape_data(self):
        self.scrape("https://pointsbet.com.au/sports/mma/UFC", name_index=-1)
        self.scrape("https://pointsbet.com.au/sports/basketball/NBA")
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Pointsbet()
    scrape_obj.write_to_csv()
