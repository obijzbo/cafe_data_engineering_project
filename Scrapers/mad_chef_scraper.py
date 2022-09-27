from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from configs.data_config import WAIT, MEDIUM_WAIT, LONG_WAIT
from functions import make_dir, cleaned
import json
from datetime import date



class MadChefScraper:
    def __init__(self, driver, data_path, link):
        self.driver = driver
        self.data_path = data_path
        self.link = link
        self.menu_link = ''
        self.raw_menu = []
        self.menu_dicts = []
        self.location_link = ''
        self.location_dict = {'mad_chef' : []}
        self.time = str(date.today())
        pass

    def open_web_page(self):
        self.driver.get(self.link)

    def get_menu_link(self):
        try:
            menu_href = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[@class="nav-bar-link " and @href="/menu"]'))
            )
            self.menu_link = menu_href.get_attribute('href')

        except Exception as e:
            print(f"Menu link not found. Error = {e}")

    def go_to_link(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_link(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def select_menu(self):
        self.get_menu_link()
        self.go_to_link(self.menu_link)

    def extract_menu_content(self):
        menu_page = requests.get(self.menu_link)
        soup = BeautifulSoup(menu_page.content, 'html.parser')
        menu_categories_1 = soup.find_all('div', class_ = 'menu-category menu-category-c3')
        for menu_category in menu_categories_1:
            title = menu_category.find_next('div', class_ = 'menu-category-title')
            title = title.get_text(strip=True)
            menu_row = menu_category.find_next('div', class_ = 'menu-row')
            list = []
            for menu_item in menu_row:
                item = []
                for string in menu_item.stripped_strings:
                    item.append(string)
                if len(item):
                    item.append(title)
                    list.append(item)
            self.raw_menu.append(list)
        menu_categories_2 = soup.find_all('div', class_='menu-category menu-category-c2')
        for menu_category in menu_categories_2:
            title = menu_category.find_next('div', class_ = 'menu-category-title')
            title = title.get_text(strip=True)
            menu_row = menu_category.find_next('div', class_ = 'menu-row')
            list = []
            for menu_item in menu_row:
                item = []
                for string in menu_item.stripped_strings:
                    item.append(string)
                if len(item):
                    item.append(title)
                    list.append(item)
            self.raw_menu.append(list)
        print(self.raw_menu)


    def convert_menu_info_into_json(self):
        for menus in self.raw_menu:
            for items in menus:
                menu_dict = {}
                menu_dict['index'] = cleaned(items[4])
                menu_dict['item_name'] = cleaned(items[2])
                menu_dict['item_description'] = cleaned(items[3])
                menu_dict['item_price'] = cleaned(items[1])
                self.menu_dicts.append(menu_dict)

        make_dir(f"{self.data_path}/{self.time}")
        with open(f"{self.data_path}/{self.time}/menu_info.json", 'w') as file:
            json.dump(self.menu_dicts, file, indent=4)


    def get_location_link(self):
        try:
            location_href = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[@class="nav-bar-link " and @href="/contact#branches"]'))
            )
            self.location_link = location_href.get_attribute('href')
        except Exception as e:
            print(f"Location link not found. Error = {e}")

    def select_location(self):
        self.get_location_link()
        self.go_to_link(self.location_link)

    def extract_location_content(self):
        location_page = requests.get(self.location_link)
        soup = BeautifulSoup(location_page.content, 'html.parser')
        branch_names = soup.find_all('div', class_ = 'branch-name')
        name_list = []
        for branch in branch_names:
            for name in branch.stripped_strings:
                name = cleaned(name)
                if "(Delivery)" in name:
                    name = name.replace("(Delivery)", "")
                    name.strip()
                    name_list.append(name)
                else:
                    name_list.append(name)
        self.location_dict['mad_chef'] = name_list

    def convert_location_info_into_json(self):
        with open(f"{self.data_path}/{self.time}/location_info.json", 'w') as file:
            json.dump(self.location_dict, file, indent=4)