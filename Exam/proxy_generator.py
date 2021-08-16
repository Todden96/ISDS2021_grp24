from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
proxies = req_proxy.get_proxy_list() #this will create proxy list

from selenium import webdriver
import random


PROXY = proxies[random.choice(range(len(proxies)))].get_address()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome = webdriver.Chrome(options=chrome_options, executable_path=r"C:\chromedriver.exe")
chrome.get("http://whatismyipaddress.com")


#
#
# PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT
#
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
#
# chrome = webdriver.Chrome(options=chrome_options, executable_path=r"C:\chromedriver.exe")
# chrome.get("http://whatismyipaddress.com")
# #
# #
# #
# # from selenium import webdriver
# #
# #
# # webdriver.DesiredCapabilities.CHROME['proxy'] = {
# #     "httpProxy": PROXY,
#     "ftpProxy": PROXY,
#     "sslProxy": PROXY,
#
#     "proxyType": "MANUAL",
#
# }
# driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe")
#
# driver.get('https://www.expressvpn.com/what-is-my-ip')
