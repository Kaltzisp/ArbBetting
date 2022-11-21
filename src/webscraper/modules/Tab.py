from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Tab(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"data-content=\"Head To Head\"(?:.|\n)*?WithoutAnimation\s}}\" style=\"\">{TEAM_ODDS}<\/div>")]

    def get_teams(self):
        matches = self.find(rf"match-name-text\">{TEAM_NAME} <\/span>")
        teams = []
        for match in matches:
            teams.extend(match.split(" v "))
        return teams

    def scrape_data(self):
        # self.scrape("https://www.tab.com.au/sports/betting/Basketball/competitions/NBA")
        self.scrape("https://www.tab.com.au/sports/betting/Soccer/competitions/2022%20World%20Cup%20Matches")


if __name__ == "__main__":
    scrape_obj = Tab()
    scrape_obj.write_to_csv()
