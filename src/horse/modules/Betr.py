from src.horse.HorseWebScraper import HorseWebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Betr(HorseWebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"No open markets available"

    def get_odds(self):
        return [float(i) for i in self.find(rf"<span>{TEAM_ODDS}<\/span>")][::2]

    def get_teams(self):
        team_list = self.find(rf"alt=\"{TEAM_NAME}\"")
        odds = [float(i) for i in self.find(rf"<span>{TEAM_ODDS}<\/span>")][::2]
        return team_list[2:len(team_list)-4][:len(odds)]

    def scrape_data(self):
        self.scrape("https://betr.com.au/racebook#/racing/2022-11-12/meeting/1006247/race/1076563")



if __name__ == "__main__":
    scrape_obj = Betr()
    scrape_obj.write_to_csv()
