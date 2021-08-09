from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def Steam_DB_Price_WebScrape(id, path2selenium='C:/chromedriver.exe', tags=True):

    """

    :param id: input str
    :param path2selenium: input stra
    :return: DataFrame
    """

    # settings for Selenium
    driver = webdriver.Chrome(path2selenium)
    driver.get('https://steamdb.info/app/'+ str(id) +'/')  # website

    driver.find_element_by_id("tab-prices").click()

    prices = driver.find_element_by_id("prices")


    tags = []

    for i in range(len(prices.find_elements_by_class_name("btn.btn-sm.btn-outline.btn-tag"))):
        tags.append(prices.find_elements_by_class_name("btn.btn-sm.btn-outline.btn-tag")[i].text)

    if 'Free to Play' in tags:
        driver.quit()


        return print("This game is free to play")

    else:
        table = driver.find_elements_by_class_name("table")[1]  # prices table

        header = table.find_elements()  # Header

        body = table.find_elements_by_tag_name("tbody")[0]  # selecting the tbody of the table

        rows = body.find_elements_by_tag_name("tr")  # finding the rows of the tbody
        column_length = rows[0].find_elements_by_tag_name("td")
        cells = body.find_elements_by_tag_name("td")

        list_db = []
        for x in range(len(rows)):
            innerlist = []
            for i in range(len(rows[x].find_elements_by_tag_name("td"))):
                innerlist.append(rows[x].find_elements_by_tag_name("td")[i].text)
            list_db.append(innerlist)

        df = pd.DataFrame(list_db)

        if tags == True:
            prices = driver.find_element_by_id("prices")

            tags = []

            for i in range(len(prices.find_elements_by_class_name("btn.btn-sm.btn-outline.btn-tag"))):
                tags.append(prices.find_elements_by_class_name("btn.btn-sm.btn-outline.btn-tag")[i].text)

            df['tags'] = ""

            for k in range(len(rows)):
                df.at[k, 'tags'] = tags

        driver.quit()

        return df

df_value = Steam_DB_Price_WebScrape(271590) # test on GTA V



df_value2 = Steam_DB_Price_WebScrape(7940) # test on CoD IV


df_value3 = Steam_DB_Price_WebScrape(570) # test on Dota 2 Free game

















