from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Betr(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"No open markets available"

    def get_odds(self):
        return [float(i) for i in self.find(rf"<span>{TEAM_ODDS}<\/span>")][:2] + [float(i) for i in self.find(rf"<span>{TEAM_ODDS}<\/span>")][6:]

    def get_teams(self):
        return self.find(rf"OddsButton_priceType__ROL\+V\">{TEAM_NAME}<")

    def get_comps(self):
        return self.find(r"href=\"#\/(sport\/[0-9]+\/competition\/[0-9]+\/[0-9]+)")

    def scrape_data(self):
        # self.scrape_all(
        #     comps_url="https://betr.com.au/sportsbook#/sport/11/all",
        #     url="https://betr.com.au/sportsbook#/%URL%",
        #     timein=1,
        #     name_index=-1
        # )
        # self.scrape("https://betr.com.au/sportsbook#/sport/6/competition/1000894/1005021")
        # self.scrape("https://betr.com.au/sportsbook#/sport/9/competition/1000226/1000520", name_index=-1)
        # self.scrape("https://betr.com.au/sportsbook#/sport/12/competition/1000492/1001891")
        self.scrape("https://betr.com.au/sportsbook#/sport/13/competition/1000649/1003042")
        # self.scrape("https://betr.com.au/sportsbook#/sport/23/competition/1000227/1000521", name_index=-1)
        # self.scrape("https://betr.com.au/sportsbook#/sport/1006/competition/1000623/1002652")


if __name__ == "__main__":
    scrape_obj = Betr()
    scrape_obj.write_to_csv()
