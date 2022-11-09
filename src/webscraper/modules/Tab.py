from src.webscraper.WebScraper import WebScraper
from selenium.webdriver.common.by import By
import logging


class Tab(WebScraper):
    def __init__(self, driver, hidden):
        super().__init__(driver, hidden)
        self.team_mapping = {
            'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2': 'G2',
            'CTBC Flying Oyster': 'CFO', 'T1 Esports': 'T1', 'EDward Gaming': 'EDG',
            'Top Esports': 'TES', 'Dwg Kia': 'DK', 'GAM Esports': 'GAM',
            '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
            'Rogue': 'RGE', 'Gen.g': 'GEN', 'Saigon Buffalo': 'SGB',
            'LOUD': 'LLL', 'Jd Gaming': 'JDG', 'Drx': 'DRX', 'Royal Never Give Up': 'RNG',
            'Evil Geniuses': 'EG', 'Fnatic': 'FNC', 'Gam': 'GAM', 'Gen.g': 'GEN', 'Edward Gaming': 'EDG',
            'Royal Never Give': 'RNG', 'T1': 'T1', 'Ctbc Flying Oyst': 'CFO'
        }
        self.nba_mapping = {
            'Boston': 'Boston Celtics',
            'Philadelphia': 'Philadelphia 76ers',
            'Golden State': 'Golden State Warriors',
            'LA Lakers': 'Los Angeles Lakers',
            'Indiana': 'Indiana Pacers',
            'Washington': 'Washington Wizards',
            'Detroit': 'Detroit Pistons',
            'Orlando': 'Orlando Magic',
            'Toronto': 'Toronto Raptors',
            'Cleveland': 'Cleveland Cavaliers',
            'Brooklyn': 'Brooklyn Nets',

            'New York': 'New York Knicks',
            'Atlanta': 'Atlanta Hawks',
            'Houston': 'Houston Rockets',
            'Memphis': 'Memphis Grizzlies',
            'Miami': 'Miami Heat',
            'Chicago': 'Chicago Bulls',
            'Minnesota': 'Minnesota Timberwolves',
            'Oklahoma City': 'Oklahoma City Thunder',
            'San Antonio': 'San Antonio Spurs',
            'Charlotte': 'Charlotte Hornets',
            'Utah': 'Utah Jazz',
            'Denver': 'Denver Nuggets',
            'Sacramento': 'Sacramento Kings',
            'Portland': 'Portland Trail Blazers',
            'Phoenix': 'Phoenix Suns',
            'Dallas': 'Dallas Mavericks',
            'Milwaukee': 'Milwaukee Bucks',
            'New Orleans': 'New Orleans Pelicans',
            'LA Clippers': 'Los Angeles Clippers'
        }

    def scrape_data(self):
        total_teams = []
        total_odds = []

        try:
            link = "https://www.tab.com.au/sports/betting/Basketball/competitions/NBA"
            self.driver.get(link)
            raw_odds = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''animate-odd''')]
            odds = []
            for odd in raw_odds:
                if odd == "SUSP":
                    odds.append(0)
                else:
                    odds.append(float(odd))
            odds = [odds[i] for i in range(len(odds)) if i % 4 in [1, 2]]
            NameVsName = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''match-name-text''')]
            teams = []

            for Name in NameVsName:
                TeamName = Name.split(" v ")
                Team1 = TeamName[0]
                Team2 = TeamName[1]
                teams.append(Team1)
                teams.append(Team2)
            teams = [self.nba_mapping[team] for team in teams]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]


if __name__ == "__main__":
    scrape_obj = Tab()
    scrape_obj.write_to_csv()
