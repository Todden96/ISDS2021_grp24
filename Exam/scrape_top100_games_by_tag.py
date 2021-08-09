# Grab 100 games within tag ID

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

def scrape_top100_games_by_tag_id(id):

    """
    :param id: integer
    :return: DataFrame
    """

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=chrome_options)
    driver.get('https://steamdb.info/tag/'+ str(id) +'/') # website

    table = driver.find_elements_by_id("table-apps")[0]

    # list_check = table.text.splitlines()

    # Header
    header_list = []
    header = table.find_elements_by_tag_name("thead")[0]  # Header
    header_items = header.find_elements_by_tag_name("th")
    for i in range(len(header_items)):
        header_list.append(header_items[i].text)


    # dimension of the table
    body = table.find_elements_by_tag_name("tbody")[0]
    rows = body.find_elements_by_tag_name("tr")  # finding the rows of the tbody
    column_length = rows[0].find_elements_by_tag_name("td")
    cells = body.find_elements_by_tag_name("td")


    list_db = []
    for x in range(len(rows)):
        innerlist = []
        for i in range(len(rows[x].find_elements_by_tag_name("td"))):
            innerlist.append(rows[x].find_elements_by_tag_name("td")[i].text)
        list_db.append(innerlist)

    id_list = []
    id = body.find_elements_by_tag_name("a")
    for i in range(len(id)):
        # print(id[i].get_attribute("href"))
        id_list.append(id[i].get_attribute("href"))

    tmp_df = pd.DataFrame(data= id_list, columns=['hyperlinks'])

    df = pd.DataFrame(data=list_db, columns=header_list).iloc[:, 1:]


    df['id'] = tmp_df['hyperlinks'].str.rsplit("/", expand=True).iloc[:, -2]


    return df