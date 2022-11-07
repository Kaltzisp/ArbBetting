from src.webscraper.WebScraper import WebScraper


class Betr(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)

    def get_odds(self):
        return [float(i) for i in self.find(r"<span>([\d\.]+)<\/span>")]

    def get_teams(self):
        return self.find(r"OddsButton_priceType__ROL\+V\">([\w|\-| ]+)<")

    def scrape_data(self):
        self.scrape("https://betr.com.au/sportsbook#/sport/9/competition/1000226/1000520", surnames_only=True)
        self.scrape("https://betr.com.au/sportsbook#/sport/11/competition/1000965/1006008", sleep_duration=1)
        self.scrape("https://betr.com.au/sportsbook#/sport/13/competition/1000649/1003042", sleep_duration=1)
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Betr()
    scrape_obj.write_to_csv()
