from website.webscraper import WebScraper
from selenium.webdriver.common.by import By

class TabH2H(WebScraper):
    def __init__(self, local):
        super().__init__(local)
        self.source = "TabH2H"
        self.team_mapping = {'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
                'CTBC Flying Oyster': 'CFO', 'T1 Esports': 'T1', 'EDward Gaming': 'EDG',
                'Top Esports': 'TES', 'DAMWON Gaming': 'DK', 'GAM Esports': 'GAM',
                '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
                'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
                'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX':'DRX', 'Royal Never Give Up':'RNG',
                'Evil Geniuses': 'EG', 'Fnatic': 'FNC', 'Gam': 'GAM', 'Gen.g': 'GEN','Edward Gaming': 'EDG',
                'Royal Never Give':'RNG', 'T1':'T1', 'Ctbc Flying Oyst': 'CFO'}

    def scrape_data(self):
        link = "https://www.tab.com.au/sports/betting/Esports/competitions/League%20of%20Legends/tournaments/LoL%20-%20World%20Championships"
        self.driver.get(link)
        odds = [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''animate-odd''')]
        NameVsName = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''match-name-text''')]
        
        teams = []

        for Name in NameVsName:
            TeamName = Name.split(" v ")
            Team1 = TeamName[0]
            Team2 = TeamName[1]
            teams.append(Team1)
            teams.append(Team2)

        teams = [self.team_mapping[team] for team in teams]

        link = "https://www.tab.com.au/sports/betting/UFC"
        self.driver.get(link)
        odds += [float(i.text) for i in self.driver.find_elements(By.CLASS_NAME, '''animate-odd''')]

        NameVsName = [i.text for i in self.driver.find_elements(By.CLASS_NAME, '''match-name-text''')]

        Teamlist = []

        for Name in NameVsName:
            TeamName = Name.split(" v ")
            Team1 = TeamName[0]
            Team2 = TeamName[1]
            Teamlist.append(Team1)
            Teamlist.append(Team2)

        for Name in Teamlist:
            if Name[-1].Upper():
                Team = Name[:-2]
            teams.append(Team)

        self.data = [(teams[i], odds[i]) for i in range(len(teams))]

if __name__ == "__main__":
    scrape_obj = TabH2H(True)
    scrape_obj.write_to_csv()

