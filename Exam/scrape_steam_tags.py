#Grabing tag ids
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

def steam_db_tag_ids():

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=chrome_options)
    driver.get('https://steamdb.info/tags/')  # website

    tags_list = driver.find_element_by_id("list")

    href = tags_list.find_elements_by_tag_name("a")

    tags_name = []
    for i in range(len(href)):
        # print(href[i].text)
        tags_name.append(href[i].text)

    list_list =[]

    for i in range(len(href)):
        list_list.append(href[i].get_attribute("href"))

    driver.quit()

    href_df = pd.DataFrame(data=list_list, columns=["hyperlinks"])

    tags_df = pd.DataFrame(tags_name, columns=['Name'])

    tags_df['id'] = href_df['hyperlinks'].str.rsplit("/", expand=True).iloc[:, -2]

    return tags_df

