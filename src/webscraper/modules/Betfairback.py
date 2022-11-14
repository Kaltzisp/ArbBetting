from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Betfairback(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"There are no events to be displayed"

    def get_odds(self):
        odds = [float(i) for i in self.find(rf"<span class=\"bet-button-price\">{TEAM_ODDS}<\/span>")]
        for i, odd in enumerate(odds):
            if odd == "":
                odds[i] = 1
        sorted_odds = odds[::2]
        return [1 + 0.95 * (odd - 1) for odd in sorted_odds]

    def get_teams(self):
        return self.find(rf"<li class=\"name\" title=\"{TEAM_NAME}\">")

    def get_comps(self):
        return self.find(r"href=\"(tennis\/competition\/[0-9]+)\">")

    def scrape_data(self):
        self.scrape_all(
            comps_url="https://www.betfair.com.au/exchange/plus/en/tennis-betting-2",
            url="https://www.betfair.com.au/exchange/plus/%URL%",
            name_index=-1
        )
        self.scrape("https://www.betfair.com.au/exchange/plus/basketball/competition/10547864")
        self.scrape("https://www.betfair.com.au/exchange/plus/american-football/competition/12282733")
        self.scrape("https://www.betfair.com.au/exchange/plus/mixed-martial-arts/competition/10581356", name_index=-1)
        self.scrape("https://www.betfair.com.au/exchange/plus/ice-hockey/competition/12300973")
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Betfairback()
    scrape_obj.write_to_csv()
