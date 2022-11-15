import logging


class log():

    def info(string):
        logging.info(string)
        print(string)

    def error(string):
        logging.exception(string)
        print(string)


TEAM_ODDS = r"([\d\.]+)"
TEAM_NAME = r"([\w\-\/',. ]+)"

TEAM_MAPPING = {"LA Clippers": "Los Angeles Clippers"}
