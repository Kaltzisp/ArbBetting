# Imports.
import time
import logging
import datetime
from os import path, mkdir
from shutil import rmtree
from glob import glob
from importlib import import_module

now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

if not path.isdir('src/webscraper/logs'):
    mkdir('src/webscraper/logs')
logging.basicConfig(filename=f'src/webscraper/logs/{now}.log', encoding='utf-8', level=logging.INFO)


def scrape_odds(hidden=False, site_list=None):
    # Setting selenium driver.
    driver = None

    # Getting module list.
    site_paths = glob(path.join("src", "webscraper", "modules", "*.py"))
    if site_list is None:
        site_list = [path.basename(site_path)[0:-3] for site_path in site_paths]
    modules = [getattr(import_module("src.webscraper.modules." + module), module) for module in site_list]

    # Clearing data files
    if path.isdir('src/webscraper/data'):
        rmtree('src/webscraper/data')
    mkdir('src/webscraper/data')

    # Running webscraper modules.
    for module in modules:
        start = time.time()
        scrape_obj = module(driver, hidden)
        try:
            logging.info(f"{module.__name__}: Attempting webscrape")
            scrape_obj.write_to_csv()
            logging.info(f"{module.__name__}: Scraped successfully")
        except Exception as e:
            logging.info(f"{module.__name__}: Scraping failed")
            logging.exception(e)
        logging.info(f"{module.__name__} scraped in {time.time() - start} secs")


if __name__ == "__main__":
    scrape_odds()
