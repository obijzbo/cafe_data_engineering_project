from Scrapers.mad_chef_scraper import MadChefScraper
from configs.data_config import ROOT_PATH,DATA_PATH
from configs.mad_chef_config import DATA_Dir,LINK

def mad_chef_data_collector(driver):
    data_path = f"{ROOT_PATH}/{DATA_PATH}/{DATA_Dir}"
    mad_chef_scraper = MadChefScraper(driver, data_path, LINK)
    mad_chef_scraper.open_web_page()
    mad_chef_scraper.select_menu()
    mad_chef_scraper.extract_menu_content()
    mad_chef_scraper.convert_menu_info_into_json()
    mad_chef_scraper.close_link()
    mad_chef_scraper.select_location()
    mad_chef_scraper.extract_location_content()
    mad_chef_scraper.convert_location_info_into_json()
    mad_chef_scraper.close_link()