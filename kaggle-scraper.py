from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from string import ascii_lowercase
import re
import urllib.request
import requests
import sys

f = open('structure.txt', 'wb')
titles = []
datafile_names = []

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-notifications')
prefs = {'download.default_directory': r'C:\xampp\htdocs\Visual-Eyes\data_files\\', 'profile.default_content_settings.popups': 0, "profile.default_content_setting_values.automatic_downloads": 1}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('C:/windows/chromedriver.exe', chrome_options=chrome_options)

driver.get('https://www.kaggle.com/account/login')

time.sleep(30)

for c in ascii_lowercase:

    driver.get('https://www.kaggle.com/datasets?search=' + c + '&sort=votes&fileType=csv&sizeStart=0%2CKB&sizeEnd=5%2CMB')
    time.sleep(1)

    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')

    for i in range(20): 
        datasets = driver.find_elements_by_xpath("//a[contains(@class, 'sc-pYOBj exUlrs')]")

        if datasets and datasets[i] is not None:
            title = datasets[i].get_attribute('title')

            if not title in titles:
                titles.append(title)
                line = title + ': '

                driver.execute_script("arguments[0].click();", datasets[i])
                time.sleep(2)

                content = driver.page_source
                soup = BeautifulSoup(content, features='html.parser')

                description = soup.find('h2', {'class':'dataset-header-v2__subtitle'}).text
                line += description + ': '

                datafiles = driver.find_elements_by_xpath("//p[contains(@class, 'sc-fzoyTs sc-fzoNJl sc-jxBrcD')]")
                
                if datafiles:
                    for k in range(0, len(datafiles)):
                        if datafiles[k] is not None:
                            file_name = datafiles[k].text
                            if not file_name in datafile_names:
                                datafile_names.append(file_name)
                                if ('.csv' in file_name):
                                    driver.execute_script("arguments[0].click();", datafiles[k])
                                    time.sleep(1)

                                    content = driver.page_source
                                    soup = BeautifulSoup(content, features='html.parser')
                                    file_size = soup.find('span', {'class':'sc-kNAOpY gTsxdh'}).text

                                    if ('KB' in file_size):
                                        line += datafiles[k].text + ', '
                                        time.sleep(1)

                                        download_link = driver.find_element_by_xpath("//i[contains(@class, 'sc-AxgMl ccBsuS sc-jRRfIE kZQbg')]")
                                        driver.execute_script("arguments[0].click();", download_link)

                    line += '\n'
                    encoded_line = line.encode(sys.stdout.encoding, errors='replace')
                    f.write(encoded_line)

        driver.get('https://www.kaggle.com/datasets?search=' + c + '&sort=votes&fileType=csv&sizeStart=0%2CKB&sizeEnd=5%2CMB')
        time.sleep(1)
        content = driver.page_source
        soup = BeautifulSoup(content, features='html.parser')