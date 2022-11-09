from src.webscraper.WebScraper import WebScraper
import re
import time
import logging


class Betright(WebScraper):
    def __init__(self, driver, hidden):
        super().__init__(driver, hidden)
        self.team_mapping = {
            'MAD Lions': "MAD", 'DetonatioN FM': 'DFM', 'G2 Esports': 'G2',
            'CTBC Flying Oyster': 'CFO', 'T1': 'T1', 'Edward Gaming': 'EDG',
            'Top Esports': 'TES', 'DWG KIA': 'DK', 'GAM Esports': 'GAM',
            '100 Thieves': '100', 'Cloud9': 'C9', 'JD Gaming': 'JDG',
            'Rogue': 'RGE', 'Gen.G': 'GEN', 'Saigon Buffalo': 'SGB',
            'LOUD': 'LLL', 'JD Gaming': 'JDG', 'DRX': 'DRX', 'Evil Geniuses': 'EG',
            'Royal Never Give Up': 'RNG', 'Fnatic': 'FNC', 'GAM Sports': 'GAM'
        }

    def scrape_data(self):
        total_odds = []
        total_teams = []

        try:
            link = '''https://www.betright.com.au/sports/Martial-Arts/128'''
            self.driver.get(link)
            time.sleep(1)
            odds = [float(i) for i in re.findall('''place-bet__odds ng-binding">([\d\.]*)<''', self.driver.page_source)]
            teams = [team.split(' ')[-1] for team in re.findall('''zeta headline-wrap ng-binding">([\w\d\.\-' ]*)<''', self.driver.page_source)]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('UFC import failed')
        total_odds += odds
        total_teams += teams

        try:
            link = '''https://www.betright.com.au/sports/Basketball/United-States-of-America/NBA/54'''
            self.driver.get(link)
            time.sleep(1)
            odds = [float(i) for i in re.findall('''place-bet__odds ng-binding">([\d\.]*)<''', self.driver.page_source)]
            teams = [team for team in re.findall('''zeta  headline-wrap ng-binding">([\w\d\.\-' ]*)<''', self.driver.page_source)]
            assert(len(odds) == len(teams))
        except Exception as e:
            odds = []
            teams = []
            logging.exception(e)
            logging.info('NBA import failed')
        total_odds += odds
        total_teams += teams
        # n_game_elements = len([i for i in self.driver.find_elements(By.CLASS_NAME, "ng-binding") if " v " in i.text])
        # for idx in range(n_game_elements):
        #     time.sleep(1)
        #     game = [i for i in self.driver.find_elements(By.CLASS_NAME, "ng-binding") if " v " in i.text][idx]
        #     game.click()
        #     self.driver.find_element(By.XPATH, '''/html/body/div[2]/div/section/div/div/ui-view/ui-view/section/div[3]/div/ul/li[2]/a/div/div[2]/span''').click()
        #     time.sleep(1)
        #     first_blood_odds = [float(i) for i in re.findall('''place-bet__odds ng-binding">([\d\.]*)<''', self.driver.page_source)][4:6]
        #     first_tower_odds = [float(i) for i in re.findall('''place-bet__odds ng-binding">([\d\.]*)<''', self.driver.page_source)][21:23]
        #     first_inhib_odds = [float(i) for i in re.findall('''place-bet__odds ng-binding">([\d\.]*)<''', self.driver.page_source)][25:27]
        #     first_blood_teams = re.findall('''g.BetDetailTypeCode === 'PLC'">([^<>]*)<''', self.driver.page_source)[4:6]
        #     first_blood_teams = [self.team_mapping[i] + ' First Blood' for i in first_blood_teams]
        #     first_tower_teams = re.findall('''g.BetDetailTypeCode === 'PLC'">([^<>]*)<''', self.driver.page_source)[21:23]
        #     first_tower_teams = [self.team_mapping[i] + ' First Tower' for i in first_tower_teams]
        #     first_inhib_teams = re.findall('''g.BetDetailTypeCode === 'PLC'">([^<>]*)<''', self.driver.page_source)[25:27]
        #     first_inhib_teams = [self.team_mapping[i] + ' First Inhib' for i in first_inhib_teams]

        #     teams += first_blood_teams + first_tower_teams + first_inhib_teams
        #     odds += first_blood_odds + first_tower_odds + first_inhib_odds
        #     self.driver.back()
        #     self.driver.back()

        self.data = [(total_teams[i], total_odds[i]) for i in range(len(total_teams))]


if __name__ == "__main__":
    scrape_obj = Betright()
    scrape_obj.write_to_csv()
