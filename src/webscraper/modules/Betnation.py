from src.webscraper.WebScraper import WebScraper
from src.utils import TEAM_ODDS, TEAM_NAME


class Betnation(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.no_markets = r"<h1>N\/A<\/h1>"

    def get_odds(self):
        return [float(i) for i in self.find(rf"transform=\"none\">{TEAM_ODDS}<\/div>")]

    def get_teams(self):
        return self.find(rf"SelectionTitleText-.*?id=\"multiBet\" transform=\"none\">{TEAM_NAME}<\/div>")

    def scrape_data(self):
        self.scrape("https://betnation.com.au/sports/basketball/nba-1000003")
        self.scrape("https://betnation.com.au/sports/american-football/nfl-1000325")
        self.scrape("https://betnation.com.au/sports/martial-arts-ufc/ultimate-fighting-championship-1000311")
        self.scrape("https://betnation.com.au/sports/tennis/open-de-roanne-auvergne-rhone-alpes-1000792", name_index=0)
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Betnation()
    scrape_obj.write_to_csv()
