from src.webscraper.WebScraper import WebScraper


class Betfairback(WebScraper):
    def __init__(self, driver=None):
        super().__init__(driver)

    def get_odds(self):
        odds = [float(i) for i in self.find(r"<span class=\"bet-button-price\">([\d\.]+)<\/span>")]
        for i, odd in enumerate(odds):
            if odd == "":
                odds[i] = 1
        odds = [1 + (odd - 1) * 0.95 for odd in odds]
        return odds[::2]

    def get_teams(self):
        return self.find(r"<li class=\"name\" title=\"([\w|\-| |\/|']+)\">")

    def scrape_data(self):
        self.scrape("https://www.betfair.com.au/exchange/plus/basketball/competition/10547864")
        self.scrape("https://www.betfair.com.au/exchange/plus/mixed-martial-arts/competition/10581356", surnames_only=True)
        self.scrape("https://www.betfair.com.au/exchange/plus/tennis/competition/12487677", surnames_only=True)
        self.data = [(self.total_teams[i], self.total_odds[i]) for i in range(len(self.total_teams))]


if __name__ == "__main__":
    scrape_obj = Betfairback()
    scrape_obj.write_to_csv()
