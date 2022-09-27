from Scrapers.pizza_hut_scraper import PizzaHutScraper
from configs.data_config import ROOT_PATH,DATA_PATH
from configs.pizza_hut_config import DATA_Dir,LINK

def pizza_hut_data_collector(driver):
    data_path = f"{ROOT_PATH}/{DATA_PATH}/{DATA_Dir}"
    pizza_hut_scraper = PizzaHutScraper(driver, data_path, LINK)
    pizza_hut_scraper.open_web_page()
    pizza_hut_scraper.select_location()
    pizza_hut_scraper.click_pizza()
    pizza_hut_scraper.pan_pizza_personal()
    pizza_hut_scraper.pan_pizza_medium()
    pizza_hut_scraper.pan_pizza_family()
    pizza_hut_scraper.cheesy_bites_medium()
    pizza_hut_scraper.cheesy_bites_family()
    pizza_hut_scraper.sausage_crust_medium()
    pizza_hut_scraper.sausage_crust_family()
    pizza_hut_scraper.thin_pizza_medium()
    pizza_hut_scraper.thin_pizza_family()
    pizza_hut_scraper.pasta_info()
    pizza_hut_scraper.appetisers_info()
    pizza_hut_scraper.deal_info()
    pizza_hut_scraper.drink_info()
    pizza_hut_scraper.convert_menu_info_into_json()
    pizza_hut_scraper.location_info()
    pizza_hut_scraper.convert_location_info_into_json()