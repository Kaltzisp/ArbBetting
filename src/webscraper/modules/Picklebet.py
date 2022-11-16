from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Picklebet(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"There are currently no active markets."

    def get_odds(self):
        return [float(i) for i in self.find(rf"Outcome-module--odds--onB1v\">{TEAM_ODDS}<\/div>")]

    def get_teams(self):
        return self.find(rf"Outcome-module--name--DgQM8\">{TEAM_NAME}<\/div>")

    def scrape_data(self):
        self.scrape("https://picklebet.com/sports/mma/betting/?page=1&tab=next", name_index=0)
        self.scrape("https://picklebet.com/sports/basketball/betting?page=1&tab=next&tour=BASKETBALL%3ANBA")
        

if __name__ == "__main__":
    scrape_obj = Picklebet()
    scrape_obj.write_to_csv()
