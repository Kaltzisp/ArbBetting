from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Betdeluxe(WebScraper):
    def __init__(self, driver, hidden):
        super().__init__(driver, hidden)
        self.no_markets = r"<h1>N\/A<\/h1>"

    def get_odds(self):
        return [float(i) for i in self.find(rf"transform=\"none\">{TEAM_ODDS}<\/div>")]

    def get_teams(self):
        return self.find(rf"SelectionTitleText-.*?id=\"multiBet\" transform=\"none\">{TEAM_NAME}<\/div>")

    def scrape_data(self):
        self.scrape("https://www.betdeluxe.com.au/sports/basketball/nba-1000059")
        self.scrape("https://www.betdeluxe.com.au/sports/american-football/nfl-1000026")
        self.scrape("https://www.betdeluxe.com.au/sports/boxing/professional-boxing-1000112", name_index=0, timeout=20)
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Betdeluxe()
    scrape_obj.write_to_csv()
