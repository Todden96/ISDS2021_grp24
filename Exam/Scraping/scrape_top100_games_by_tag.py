# Grab 100 games within tag ID
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from tqdm import tqdm
import os

# id = 1003823

os.chdir(r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\ISDS')


tags_df = pd.read_csv('tags_all.csv', sep=";")

tags_id = [*tags_df['id']]

def scrape_top100_games_by_tag_id(id):

    """
    :param id: integer
    :return: DataFrame
    """
    options = Options()
    options.add_argument("--window-position=2000,0")
    # options.add_argument('--blink-settings=imagesEnabled=false')
    # options.add_argument("--start-maximized")
    url = 'https://steamdb.info/tag/'+ str(id) +'/'
    print(url)
    driver = webdriver.Chrome('C:/chromedriver.exe', options=options)
    driver.get(url) # website

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

    driver.close()

    tmp_df = pd.DataFrame(data= id_list, columns=['hyperlinks'])

    df = pd.DataFrame(data=list_db, columns=header_list).iloc[:, 1:]

    df['id'] = tmp_df['hyperlinks'].str.rsplit("/", expand=True).iloc[:, -2]

    df = df[(pd.to_numeric(df['Online'], errors='coerce') != 0) | (pd.to_numeric(df['Peak'], errors='coerce') != 0)] # check to see if there are any unpublished games in the DataFrame



    return df

# Finding all DataFrame IDs already downloaded
path = r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\ISDS\tags_all'
csvtable_list = []
id_check_list = []
os.chdir(path)
for filename in os.listdir(path):
    if filename.endswith('.csv'):
        # csvtable_list.append(pd.read_csv(filename,sep=","))
        id_check_list.append(filename[:-4].split("_")[2])



for item in tqdm(tags_id):
    if str(item) not in id_check_list:
        scrape_top100_games_by_tag_id(item).to_csv('dataframe_id_' + str(item) +'_' + tags_df.loc[tags_df['id'] == item].iloc[0,0] + '.csv', )

