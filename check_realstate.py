import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

url = 'https://www.realtor.com/realestateagents/catherine-qian_los-altos_ca_549162_150199108'

options = Options()
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--disable-extensions")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')
# options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome()
driver.get(url)


#listings arrow down
WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="review"]/div[2]/i')))
driver.find_element_by_xpath('//*[@id="review"]/div[2]/i').click()
time.sleep(2)


#on market
onmarket_url_list=[]
for i in range(1,5):
    try:
        driver.find_element_by_xpath('//*[@id="collapseOne5"]/div[2]/div/div[2]/div['+str(i)+']/div/div[1]/div').click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        onmarket_url_list.append(driver.current_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
    except:
        break

print(onmarket_url_list)

#off market
offmarket_url_list=[]
for i in range(1,5):
    try:
        driver.find_element_by_xpath('//*[@id="collapseOne5"]/div[3]/div/div[2]/div['+str(i)+']/div/div[1]/div').click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        offmarket_url_list.append(driver.current_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
    except:
        break

print(offmarket_url_list)

