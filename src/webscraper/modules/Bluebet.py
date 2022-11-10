from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Bluebet(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"<div class=\"jss[0-9]+\">(?![\d\.+-])[\w -'\.]+<\/div>\s*{TEAM_ODDS}\s*<\/div>")]

    def get_teams(self):
        return self.find(rf"Typography-noWrap\">{TEAM_NAME}<\/h2>")

    def scrape_data(self):
        self.scrape("https://www.bluebet.com.au/sports/Rugby-Union/105/World/Rugby-Union-Internationals/38823")
        self.scrape("https://www.bluebet.com.au/sports/Basketball/107/United-States-of-America/NBA-Matches/39251")
        self.scrape("https://www.bluebet.com.au/sports/American-Football/108/United-States-of-America/NFL-Matches/37249")
        self.scrape("https://www.bluebet.com.au/sports/Tennis/104/France/Open-International-De-Tennis-De-Roanne/114907", name_index=-1)
        self.scrape("https://www.bluebet.com.au/sports/Tennis/104/Slovakia/Peugeot-Slovak-Open-2/114896", name_index=-1)
        self.scrape("https://www.bluebet.com.au/sports/Ice-Hockey/111")
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Bluebet()
    scrape_obj.write_to_csv()
