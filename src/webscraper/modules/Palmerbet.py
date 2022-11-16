from src.webscraper.WebScraper import WebScraper
from src.core.utils import TEAM_ODDS, TEAM_NAME


class Palmerbet(WebScraper):
    def __init__(self, driver=None, hidden=False):
        super().__init__(driver, hidden)
        self.no_markets = r"NO MARKETS AVAILABLE"

    def get_odds(self):
        return [float(i) for i in self.find(rf"alt-button-design.*?>{TEAM_ODDS}<\/div>")]

    def get_teams(self):
        return self.find(rf"class=\"team-name\"> {TEAM_NAME} <\/span>")

    def scrape_data(self):
        self.scrape("https://www.palmerbet.com/sports/martial-arts/Ultimate%20Fighting%20Championship/7ee8e39f-6bec-45c1-b484-28023ce0dfce", name_index=0)
        self.scrape("https://www.palmerbet.com/sports/basketball/NBA/b26e5acc-02ff-4b22-ae69-0491fbd2500e")


if __name__ == "__main__":
    scrape_obj = Palmerbet()
    scrape_obj.write_to_csv()
