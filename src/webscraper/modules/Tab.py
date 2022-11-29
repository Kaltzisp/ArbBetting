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
        self.scrape("https://www.tab.com.au/sports/betting/Basketball/competitions/NBA")
        self.scrape("https://www.tab.com.au/sports/betting/Boxing/competitions/Boxing")
        self.scrape("https://www.tab.com.au/sports/betting/Tennis/competitions/Challenger/tournaments/Challenger%20Maia")
        self.scrape("https://www.tab.com.au/sports/betting/Tennis/competitions/Challenger/tournaments/Challenger%20Andria")
        self.scrape("https://www.tab.com.au/sports/betting/American%20Football/competitions/NFL")
        self.scrape("https://www.tab.com.au/sports/betting/Tennis/competitions/Challenger/tournaments/Challenger%20Maspalomas")


if __name__ == "__main__":
    scrape_obj = Tab()
    scrape_obj.write_to_csv()
