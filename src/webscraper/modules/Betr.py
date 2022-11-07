from src.webscraper.WebScraper import WebScraper
from src.utils import TEAM_ODDS, TEAM_NAME


class Betr(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.no_markets = r"No open markets available"

    def get_odds(self):
        return [float(i) for i in self.find(rf"<span>{TEAM_ODDS}<\/span>")]

    def get_teams(self):
        return self.find(rf"OddsButton_priceType__ROL\+V\">{TEAM_NAME}<")

    def scrape_data(self):
        self.scrape("https://betr.com.au/sportsbook#/sport/9/competition/1000226/1000520", name_index=-1)
        self.scrape("https://betr.com.au/sportsbook#/sport/11/competition/1000965/1006008", name_index=-1)
        self.scrape("https://betr.com.au/sportsbook#/sport/11/competition/1000974/1006033", name_index=-1)
        self.scrape("https://betr.com.au/sportsbook#/sport/12/competition/1000492/1001891")
        self.scrape("https://betr.com.au/sportsbook#/sport/13/competition/1000649/1003042")
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Betr()
    scrape_obj.write_to_csv()
