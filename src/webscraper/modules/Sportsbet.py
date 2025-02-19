from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Sportsbet(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"<span .*?price-text\">{TEAM_ODDS}<\/span>")]

    def get_teams(self):
        return self.find(rf"(?:outcome-name|participantText).*?>{TEAM_NAME}<\/(?:span|div)>")

    def scrape_data(self):
        self.scrape("https://www.sportsbet.com.au/betting/ufc-mma", name_index=-1)
        self.scrape("https://www.sportsbet.com.au/betting/basketball-us")
        self.scrape("https://www.sportsbet.com.au/betting/tennis/atp-bratislava-challenger", name_index=-1)
        self.scrape("https://www.sportsbet.com.au/betting/tennis/atp-roanne-challenger", name_index=-1)
        self.scrape("https://www.sportsbet.com.au/betting/tennis/wta-colina-125k", name_index=-1)
        self.scrape("https://www.sportsbet.com.au/betting/ice-hockey-us")


if __name__ == "__main__":
    scrape_obj = Sportsbet()
    scrape_obj.write_to_csv()
