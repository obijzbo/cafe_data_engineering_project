from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from configs.data_config import MINI_WAIT, WAIT, MEDIUM_WAIT, LONG_WAIT, LOCATION
from functions import make_dir, cleaned
import json
import time
from datetime import date


class PizzaHutScraper:
    def __init__(self, driver, data_path, link):
        self.driver = driver
        self.data_path = data_path
        self.link = link
        self.category = ''
        self.item_name = ''
        self.item_description = ''
        self.item_price = ''
        self.pizza_link = []
        self.raw_menu = []
        self.menu_dicts = []
        self.location_link = ''
        self.location_dict = {'pizza_hut': []}
        self.time = str(date.today())
        pass

    def open_web_page(self):
        self.driver.get(self.link)

    def go_to_link(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_link(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def select_location(self):
        try:
            search_location_box = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//input[@type="text" and @class="search_location"]'))
            )
            search_location_box.click()
        except Exception as e:
            print(f"Error - {e}")
        try:
            search_box = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//input[@type="text" and @class="tawhid_modal_search_location pac-target-input"]'))
            )
            search_box.click()
            search_box.clear()
            search_box.send_keys(LOCATION)
            time.sleep(MINI_WAIT)
            search_box.send_keys(Keys.ARROW_DOWN)
            search_box.send_keys(Keys.ENTER)
            time.sleep(MINI_WAIT)
        except Exception as e:
            print(f"Error - {e}")

    def click_pizza(self):
        try:
            category_element = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//a[@class="nav-link active" and @href="https://www.pizzahutbd.com/pizza/all"]'))
            )
            category = category_element.text
            self.category = category
            print(category)
            category_element.click()
        except Exception as e:
            print(f"Error - {e}")
        pass

    def click_pan_pizza(self):
        pan_pizza = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="pn-ProductNav_Link" and @href="https://www.pizzahutbd.com/pizza/categories/2"]'))
        )
        pan_pizza_link = pan_pizza.get_attribute('href')
        self.go_to_link(pan_pizza_link)
        # pan_pizza.click()
        pass

    def pan_pizza_personal(self):
        self.click_pan_pizza()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        # personals = WebDriverWait(self.driver, WAIT).until(
        #         EC.presence_of_all_elements_located(
        #             (By.XPATH,
        #              '//div[@class="col col-lg col-sm-12" and @style="border-left:3px solid white;"]'))
        #     )
        # personals = self.driver.find_elements(By.XPATH,
        #                                       '//div[@class="col col-lg col-sm-12" and @style="border-left:3px solid white;"]')
        # time.sleep(WAIT)
        # for personal in personals:
        #     personal.click()
        #     print("Clicking personal!!!!!!!!!!!!")
        #     time.sleep(MINI_WAIT)
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name + " " + "Personal"
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def pan_pizza_medium(self):
        self.click_pan_pizza()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        # mediums = WebDriverWait(self.driver, WAIT).until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH,
        #          '//div[@class="col col-lg col-sm-12"]'))
        # )
        mediums = self.driver.find_elements(By.XPATH, '//div[@class="col col-lg col-sm-12"]')
        time.sleep(WAIT)
        for medium in mediums:
            medium.click()
            print("Clicking medium!!!!!!!!!!!!")
            time.sleep(MINI_WAIT)
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name + " " + "Medium"
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def pan_pizza_family(self):
        self.click_pan_pizza()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        # families = WebDriverWait(self.driver, WAIT).until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH,
        #          '//div[@class="col col-lg col-sm-12" and @style="border-right:3px solid white"]'))
        # )
        families = self.driver.find_elements(By.XPATH,
                                             '//div[@class="col col-lg col-sm-12" and @style="border-right:3px solid white"]')
        time.sleep(WAIT)
        for family in families:
            family.click()
            print("Clicking family!!!!!!!!!!!!")
            time.sleep(MINI_WAIT)
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name + " " + "Family"
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def click_cheesy_bites(self):
        cheesy_bites = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="pn-ProductNav_Link" and @href="https://www.pizzahutbd.com/pizza/categories/10"]'))
        )
        cheesy_bites_link = cheesy_bites.get_attribute('href')
        self.go_to_link(cheesy_bites_link)
        pass

    def cheesy_bites_medium(self):
        self.click_cheesy_bites()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        # mediums = WebDriverWait(self.driver, WAIT).until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH,
        #          '//div[@class="col col-lg col-sm-12"]'))
        # )
        # mediums = self.driver.find_elements(By.XPATH, '//div[@class="col col-lg col-sm-12"]')
        # time.sleep(WAIT)
        # for medium in mediums:
        #     medium.click()
        #     print("Clicking medium!!!!!!!!!!!!")
        #     time.sleep(MINI_WAIT)
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name + " " + "Medium"
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def cheesy_bites_family(self):
        self.click_cheesy_bites()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        # families = WebDriverWait(self.driver, WAIT).until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH,
        #          '//div[@class="col col-lg col-sm-12" and @style="border-right:3px solid white"]'))
        # )
        families = self.driver.find_elements(By.XPATH,
                                             '//div[@class="col col-lg col-sm-12" and @style="border-right:3px solid white"]')
        time.sleep(WAIT)
        for family in families:
            family.click()
            print("Clicking family!!!!!!!!!!!!")
            time.sleep(MINI_WAIT)
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name + " " + "Family"
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def click_sausage_crust(self):
        sausage_crust = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="pn-ProductNav_Link" and @href="https://www.pizzahutbd.com/pizza/categories/11"]'))
        )
        sausage_crust_link = sausage_crust.get_attribute('href')
        self.go_to_link(sausage_crust_link)
        pass

    def sausage_crust_medium(self):
        self.click_sausage_crust()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        # mediums = WebDriverWait(self.driver, WAIT).until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH,
        #          '//div[@class="col col-lg col-sm-12"]'))
        # )
        # mediums = self.driver.find_elements(By.XPATH, '//div[@class="col col-lg col-sm-12"]')
        # time.sleep(WAIT)
        # for medium in mediums:
        #     medium.click()
        #     print("Clicking medium!!!!!!!!!!!!")
        #     time.sleep(MINI_WAIT)
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name + " " + "Medium"
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def sausage_crust_family(self):
        self.click_sausage_crust()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        # families = WebDriverWait(self.driver, WAIT).until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH,
        #          '//div[@class="col col-lg col-sm-12" and @style="border-right:3px solid white"]'))
        # )
        families = self.driver.find_elements(By.XPATH,
                                             '//div[@class="col col-lg col-sm-12" and @style="border-right:3px solid white"]')
        time.sleep(WAIT)
        for family in families:
            family.click()
            print("Clicking family!!!!!!!!!!!!")
            time.sleep(MINI_WAIT)
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name + " " + "Family"
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def click_thin_pizza(self):
        thin_pizza = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="pn-ProductNav_Link" and @href="https://www.pizzahutbd.com/pizza/categories/12"]'))
        )
        thin_pizza_link = thin_pizza.get_attribute('href')
        self.go_to_link(thin_pizza_link)
        pass

    def thin_pizza_medium(self):
        self.click_thin_pizza()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        # mediums = WebDriverWait(self.driver, WAIT).until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH,
        #          '//div[@class="col col-lg col-sm-12"]'))
        # )
        # mediums = self.driver.find_elements(By.XPATH, '//div[@class="col col-lg col-sm-12"]')
        # time.sleep(WAIT)
        # for medium in mediums:
        #     medium.click()
        #     print("Clicking medium!!!!!!!!!!!!")
        #     time.sleep(MINI_WAIT)
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name + " " + "Medium"
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def thin_pizza_family(self):
        self.click_thin_pizza()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        # families = WebDriverWait(self.driver, WAIT).until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH,
        #          '//div[@class="col col-lg col-sm-12" and @style="border-right:3px solid white"]'))
        # )
        families = self.driver.find_elements(By.XPATH,
                                             '//div[@class="col col-lg col-sm-12" and @style="border-right:3px solid white"]')
        time.sleep(WAIT)
        for family in families:
            family.click()
            print("Clicking family!!!!!!!!!!!!")
            time.sleep(MINI_WAIT)
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name + " " + "Family"
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def click_pasta(self):
        category_element = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="nav-link" and @href="https://www.pizzahutbd.com/pasta/all"]'))
        )
        category = category_element.text
        self.category = category
        print(category)

        pasta = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="nav-link" and @href="https://www.pizzahutbd.com/pasta/all"]'))
        )
        pasta_link = pasta.get_attribute('href')
        self.go_to_link(pasta_link)
        pass

    def pasta_info(self):
        self.click_pasta()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="info"]//div[@class="price-info"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def click_appetisers(self):
        category_element = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="nav-link" and @href="https://www.pizzahutbd.com/appetisers/all"]'))
        )
        category = category_element.text
        self.category = category
        print(category)

        appetisers = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="nav-link" and @href="https://www.pizzahutbd.com/appetisers/all"]'))
        )
        appetisers_link = appetisers.get_attribute('href')
        self.go_to_link(appetisers_link)
        pass

    def appetisers_info(self):
        self.click_appetisers()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//button[@class="btn btn-success add_button addToPrizeCart"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def click_deals(self):
        category_element = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="nav-link" and @href="https://www.pizzahutbd.com/deals/all"]'))
        )
        category = category_element.text
        self.category = category
        print(category)

        deals = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="nav-link" and @href="https://www.pizzahutbd.com/deals/all"]'))
        )
        deals_link = deals.get_attribute('href')
        self.go_to_link(deals_link)
        pass

    def deal_info(self):
        self.click_deals()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="deal-item-name"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="deal-item-desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="deal-price"]//span[@class="pro_price"]'))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def click_drinks(self):
        category_element = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="nav-link" and @href="https://www.pizzahutbd.com/drinks/all"]'))
        )
        category = category_element.text
        self.category = category
        print(category)

        drinks = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//a[@class="nav-link" and @href="https://www.pizzahutbd.com/drinks/all"]'))
        )
        drinks_link = drinks.get_attribute('href')
        self.go_to_link(drinks_link)
        pass

    def drink_info(self):
        self.click_drinks()
        item_name_list = []
        item_description_list = []
        item_price_list = []
        item_names = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//div[@class="left-con-pizzas"]'))
        )
        for item_name in item_names:
            item_name_list.append(item_name.text)

        item_descriptions = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//p[@class="short_desc"]'))
        )
        for item_description in item_descriptions:
            item_description_list.append(item_description.text)

        item_prices = WebDriverWait(self.driver, WAIT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//button[@type="button" and @class="btn btn-success add_button addToPrizeCart"]//span[@class="pro_price"]' ))
        )
        for item_price in item_prices:
            item_price_list.append(item_price.text)

        for name, des, price in zip(item_name_list, item_description_list, item_price_list):
            menu_dict = {}
            menu_dict['index'] = self.category
            menu_dict['item_name'] = name
            menu_dict['item_description'] = des
            menu_dict['item_price'] = price
            self.menu_dicts.append(menu_dict)
        self.driver.refresh()
        self.close_link()
        time.sleep(WAIT)
        pass

    def convert_menu_info_into_json(self):
        make_dir(f"{self.data_path}/{self.time}")
        with open(f"{self.data_path}/{self.time}/menu_info.json", 'w') as file:
            json.dump(self.menu_dicts, file, indent=4)

    def location_info(self):
        locations = ["Banasree","Dhanmondi","Gulshan","Mirpur","Shewrapara","Uttara","Wari"]
        self.location_dict["pizza_hut"] = locations

    def convert_location_info_into_json(self):
        with open(f"{self.data_path}/{self.time}/location_info.json", 'w') as file:
            json.dump(self.location_dict, file, indent=4)