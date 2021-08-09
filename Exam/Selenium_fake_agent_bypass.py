from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager


### Counter UserAgent detection

def Selenium_fake_agent(url):
    assert url == type(str)


    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)

    options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    return driver.get(url)