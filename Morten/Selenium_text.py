import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver



driver = webdriver.Chrome('C:/chromedriver.exe')
driver.get("https://steamdb.info/app/1139900/")



spec_name=[]
spec_item=[]
driver = webdriver.Chrome()
i = "1139900"
base_url = str("https://steamdb.info/app/"+ str(i) +"/")
driver.get(base_url)
tables=WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@id='collapseSpecs']//table")))
for table in tables:
    for row in table.find_elements_by_xpath(".//tr"):
        spec_name.append(row.find_element_by_xpath('./th').get_attribute('textContent'))
        spec_item.append(row.find_element_by_xpath('./td/span').get_attribute('textContent'))

df = pd.DataFrame({"Spec_Name":spec_name,"Spec_Title":spec_item})

print(df)

