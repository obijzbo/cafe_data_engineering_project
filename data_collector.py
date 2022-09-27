from selenium import webdriver
import chromedriver_autoinstaller
from data_collection.mad_chef_data_collection import mad_chef_data_collector
from data_collection.pizza_hut_data_collection import pizza_hut_data_collector


chromedriver_autoinstaller.install(cwd=True)
driver = webdriver.Chrome()
driver.maximize_window()

mad_chef_data_collector(driver)
pizza_hut_data_collector(driver)