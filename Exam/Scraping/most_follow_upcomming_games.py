#Grabing tag ids
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

#Most Followed Upcomming

def MostFollwedUpcomming():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=chrome_options)
    driver.get('https://steamdb.info/upcoming/mostfollowed/')  # website



    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[3]/table/thead/tr/th[6]").click()

    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[3]/table/thead/tr/th[6]").click()


    table = driver.find_elements_by_class_name("table-products.table-responsive-flex.table-hover.text-left")[0]

    header = table.find_elements_by_tag_name("th") # Header

    header_list =[]

    for i in range(len(header)):
        header_list.append(header[i].text)

    rows = table.find_elements_by_tag_name("tr")[1:]  # Slicing is done to remove the header

    upcomming_db = []
    for x in range(len(rows)):
        innerlist = []
        for i in range(len(rows[x].find_elements_by_tag_name("td"))):
            innerlist.append(rows[x].find_elements_by_tag_name("td")[i].text)
        upcomming_db.append(innerlist)

    df_upcomming = pd.DataFrame(upcomming_db, columns=header_list)

    driver.close()

    df_upcomming = df_upcomming.drop(df_upcomming.columns[[0, 3, -1]], axis=1)

    df_upcomming['Name'] = df_upcomming['Name'].str.rstrip("\nGame")


    return df_upcomming

df_upcome = MostFollwedUpcomming() # tester
