from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Playup(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"There are currently no active markets."

    def get_odds(self):
        return [float(i) for i in self.find(rf"<div>{TEAM_ODDS}<\/div>")]

    def get_teams(self):
        return self.find(rf"md:text-base\">{TEAM_NAME} <\/div>")

    def scrape_data(self):
        self.scrape("https://www.playup.com.au/betting/sports/mixed-martial-arts/ufc", name_index=-1)
        self.scrape("https://www.playup.com.au/betting/sports/basketball/nba")
        

if __name__ == "__main__":
    scrape_obj = Playup()
    scrape_obj.write_to_csv()
