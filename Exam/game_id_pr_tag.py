from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import ccy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# id = 1072420
from ISDS2021_grp24.Exam.Selenium_fake_agent_bypass import Selenium_fake_agent


def Steam_DB_Price_WebScrape(id, path2selenium='C:/chromedriver.exe', tags=True, selenium_options_argument="--window-position=2000,0"):

    """

    :param id: input str
    :param path2selenium: input stra
    :return: DataFrame
    """

    # settings for Selenium
    chrome_options = Options()
    chrome_options.add_argument(selenium_options_argument)
    driver = webdriver.Chrome(path2selenium, options=chrome_options)
    #Selenium_fake_agent()
    driver.get('https://steamdb.info/app/'+ str(id) +'/')  # website

    driver.find_element_by_id("tab-prices").click()

    # prices = WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.ID, "prices"))
    prices = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.ID,"prices")))[0]

    tags = []

    for i in range(len(prices.find_elements_by_class_name("btn.btn-sm.btn-outline.btn-tag"))):
        tags.append(prices.find_elements_by_class_name("btn.btn-sm.btn-outline.btn-tag")[i].text)

    if 'Free to Play' in tags:
        driver.quit()


        return print(" This Steam game is free to play")

    else:
        table = driver.find_elements_by_class_name("table")[1]  # prices table

        if table.text == '':

            return print(f" Steam game: {id} has no prices")

        else:

            # Header
            header_list = []
            header = table.find_elements_by_tag_name("thead")[0]  # Header
            header_items = header.find_elements_by_tag_name("th")
            for i in range(len(header_items)):
                header_list.append(header_items[i].text)

            body = table.find_elements_by_tag_name("tbody")[0]  # selecting the tbody of the table

            rows = body.find_elements_by_tag_name("tr")  # finding the rows of the tbody
            column_length = len(rows[0].find_elements_by_tag_name("td"))
            cells = body.find_elements_by_tag_name("td")

            list_db = []

            if len(rows[0].find_elements_by_tag_name("td")) == 5:

                for x in range(len(rows)):
                    innerlist = []
                    for i in range(len(rows[x].find_elements_by_tag_name("td"))-1):
                        innerlist.append(rows[x].find_elements_by_tag_name("td")[i].text)
                    list_db.append(innerlist)

                df = pd.DataFrame(list_db)

                df = pd.DataFrame(data=df.iloc[:, [0, 1, 2, 3]])

                df.columns = header_list[0:(df.shape[1])]

            elif len(rows[0].find_elements_by_tag_name("td")) == 6:

                for x in range(len(rows)):
                    innerlist = []
                    for i in range(len(rows[x].find_elements_by_tag_name("td"))):
                        innerlist.append(rows[x].find_elements_by_tag_name("td")[i].text)
                    list_db.append(innerlist)

                df = pd.DataFrame(list_db)

                df = pd.DataFrame(data=df.iloc[:, [0, 1, 2, 4]])

                df.columns = header_list[0:(df.shape[1])]

            elif len(rows[0].find_elements_by_tag_name("td")) == 4:

                for x in range(len(rows)):
                    innerlist = []
                    for i in range(len(rows[x].find_elements_by_tag_name("td"))-1):
                        innerlist.append(rows[x].find_elements_by_tag_name("td")[i].text)
                    list_db.append(innerlist)

                df = pd.DataFrame(list_db)

                df = pd.DataFrame(data=df.iloc[:, [0, 1, 2, 4]])

                df.columns = header_list[0:(df.shape[1])]


            df = df.fillna(0)

            df["CURRENT PRICE"] = df["CURRENT PRICE"].replace(to_replace=r'N/A', value='0', regex=True)

            df["LOWEST RECORDED PRICE"] = df["LOWEST RECORDED PRICE"].replace(to_replace=r'N/A', value='0', regex=True)

            df["CONVERTED PRICE"] = df["CONVERTED PRICE"].replace(to_replace=r'N/A', value='0', regex=True)


            df["LOWEST RECORDED PRICE"] = df.loc[df["LOWEST RECORDED PRICE"].str.contains('%'), 'CONVERTED PRICE'] = '0'



            df["CONVERTED PRICE"] = \
            df["CONVERTED PRICE"].str.rsplit("€", expand=False).map(lambda x: x[0])

            df["CONVERTED PRICE"] =df["CONVERTED PRICE"].replace(to_replace=r'--', value='00', regex=True)

            df["CONVERTED PRICE"] = df["CONVERTED PRICE"].replace(to_replace=r',', value='.', regex=True)

            df["CONVERTED PRICE"] = df["CONVERTED PRICE"].replace(to_replace=r'N/A', value='0', regex=True)


            df["CONVERTED PRICE"] = df["CONVERTED PRICE"].astype(float)

            df['CONVERTED PRICE CCY'] = str(ccy.currency('eur'))


            df["LOWEST RECORDED PRICE"] = \
            df["LOWEST RECORDED PRICE"].str.rsplit("€", expand=False).map(lambda x: x[0])

            df["LOWEST RECORDED PRICE"] =df["LOWEST RECORDED PRICE"].replace(to_replace=r'--', value='00', regex=True)

            df["LOWEST RECORDED PRICE"] = df["LOWEST RECORDED PRICE"].replace(to_replace=r',', value='.', regex=True)

            df["LOWEST RECORDED PRICE"] = df["LOWEST RECORDED PRICE"].astype(float)

            df["LOWEST RECORDED PRICE CCY"] =str(ccy.currency('eur'))

            # CCY to Float

            list_ccy_test = pd.DataFrame()

            list_ccy_test['One'] = df['CURRENT PRICE'].replace(to_replace=r',', value='.',
                                                                          regex=True).str.extract(r'(\d+.\d+)').astype(
                'float')

            list_ccy_test['Two'] = df['CURRENT PRICE'].replace(to_replace=r',', value='.',
                                                                          regex=True).str.extract(r'(\d+)').astype('float')

            list_ccy_test.loc[list_ccy_test['One'] >= list_ccy_test['Two'], 'Three'] = list_ccy_test['One']

            list_ccy_test.loc[list_ccy_test['Three'].isnull() == True, 'Three'] = list_ccy_test['Two']

            df['CURRENT PRICE'] = round(list_ccy_test['Three'], 2)




            if tags == True:
                prices = driver.find_element_by_id("prices")

                tags = []

                for i in range(len(prices.find_elements_by_class_name("btn.btn-sm.btn-outline.btn-tag"))):
                    tags.append(prices.find_elements_by_class_name("btn.btn-sm.btn-outline.btn-tag")[i].text)

                df['tags'] = ""

                for k in range(len(rows)):
                    df.at[k, 'tags'] = tags

            os.chdir(r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\ISDS\Data')
            df.to_csv('dataframe_id_' + str(id) + '.csv')

            driver.quit()

    return df



# df_value = Steam_DB_Price_WebScrape(271590) # test on GTA V
#
# df_value2 = Steam_DB_Price_WebScrape(7940) # test on CoD IV
#
#
# df_value3 = Steam_DB_Price_WebScrape(570) # test on Dota 2 Free game
