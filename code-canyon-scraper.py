from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-notifications')
driver = webdriver.Chrome('C:/windows/chromedriver.exe', chrome_options=chrome_options)

names = []
tags = []
prices = []
sales = []
revenues = []
created = []

for i in range(1,60):

    driver.get("https://codecanyon.net/category/wordpress?page=" + str(i) + "&sort=sales")

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    for a in soup.findAll(attrs={'class':'_1cn3x'}):
        name = a.find('a', attrs={'class':'_2Pk9X'})
        tag = a.find('span', attrs={'class':'_3Q47d'})
        price = a.find('div', attrs={'class':'-DeRq'})
        sale = a.find('div', attrs={'class':'_3QV9M'})

        if tag is not None:
            tags.append(tag.text)
        else:
            tags.append(' ')

        if price is not None:
            price = float(price.text.replace('$',''))
            prices.append(price)
        else:
            prices.append(0)

        if sale is not None:
            sale = sale.text
            if 'K' in sale:
                sale = float(sale.split('K')[0]) * 1000
            else:
                sale = float(sale.split(' ')[0])
            sales.append(sale)
        else:
            sales.append(0)

        if price is not None and sale is not None:
            revenues.append(sale*price)
        else:
            revenues.append(0)

        if name is not None:
            names.append(name.text)
            clickable = driver.find_element_by_xpath("//a[contains(@class, '_2Pk9X') and contains(text(), '" + name.text + "')]")
            if clickable is not None:
                clickable.click()
                time.sleep(3)
                date_field = driver.find_element_by_xpath("//td[contains(@class, 'meta-attributes__attr-detail')]")
                date = date_field.find_element_by_xpath("//span")
                if date is not None:
                    created.append(date.text)
                else:
                    created.append(' ')
                driver.back()
                time.sleep(3)
        else:
            names.append(' ')

df = pd.DataFrame({'Plugin Name':names,'Price':prices,'Sales':sales,'Revenue':revenues,'Tags':tags})
df.to_csv('plugins.csv', mode='a', header=0, index=False, encoding='utf-8')