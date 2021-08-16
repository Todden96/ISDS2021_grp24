import pandas as pd
from random import randint
from time import sleep
from tqdm import tqdm
import os
from multiprocessing import Pool
import csv


from ISDS2021_grp24.Exam.grab_game_price_data import Steam_DB_Price_WebScrape
from ISDS2021_grp24.Exam.scrape_top100_games_by_tag import scrape_top100_games_by_tag_id

os.chdir(r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\ISDS')
tags_df = pd.read_csv("tags.csv")


# saved_list = []


for i in tqdm(range(len(tags_df))) :
    action_id = tags_df.iloc[i, 1]
    action_id_df = scrape_top100_games_by_tag_id(action_id)
    print('\n')
    print(f' Now looking at the tag: {tags_df.iloc[i, 0]}')
    print('\n')





    # Finding all DataFrame IDs already downloaded
    path = r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\ISDS\Data'
    csvtable_list = []
    id_check_list = []
    os.chdir(path)
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            csvtable_list.append(pd.read_csv(filename,sep=","))
            id_check_list.append(filename[:-4].split("_")[2])
    os.chdir(r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\ISDS')
    processed_id_list = pd.read_csv("list.csv")
    saved_list = [*processed_id_list.iloc[:, 0]] + id_check_list
    print('\n')
    print(f'No. of Ids processed :  {len(saved_list)} ')
    print('\n')

    category_id = [*action_id_df.iloc[:, 5]]

    category_name = [*action_id_df.iloc[:, 0]]

    price_dict = {}


    for id in tqdm([*action_id_df.iloc[:, 5]]):
        #Dynamically create Data frames

        if id not in saved_list:   # checks if the DataFrame has already been downloaded
            sleep(0.75)


            try:
                price_dict[id] = Steam_DB_Price_WebScrape(id)
                print('\n')
                print(f' SteamDB id: {id} ')
            except:
                pass
            if isinstance(price_dict[id], pd.DataFrame): # checks if there is a valid dataframe
                os.chdir(r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\ISDS\Data')
                price_dict[id].to_csv('dataframe_id_'+str(id)+'.csv')

    saved_list.append(id)
    os.chdir(r'C:\Users\Johan\OneDrive - University of Copenhagen\8. Semester\ISDS')
    df_csv = pd.DataFrame(saved_list)
    df_csv.to_csv('list.csv', index=False, header=False)





