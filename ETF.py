from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys
import itertools
from string import printable
import time

#select Firefox as the webrowser to use and defines it as driver

#fp = webdriver.FirefoxProfile()
#fp.set_preference("http.response.timeout", 5)
#fp.set_preference("dom.max_script_run_time", 5)
#driver = webdriver.Firefox(firefox_profile=fp)
driver = webdriver.Chrome('C:\Python27\chromedriver.exe')
wait = WebDriverWait(driver, 20)

driver.get("https://finance.yahoo.com/quote/TUR/history?period1=1206680400&period2=1546063200&interval=1d&filter=history&frequency=1d")
ele = driver.find_element_by_css_selector('tr.Fz\(s\):nth-child(1)')
wait.until(EC.visibility_of(ele))
eles = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr')
i = len(eles)
getdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/span').get_attribute('innerHTML')
y = 4000
trade = False
while not ("2008" in getdate):
    driver.execute_script("window.scrollTo(0, " + str(y)+ ")")
    eles = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr')
    i = len(eles)
    y = y + 4000
    getdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/span').get_attribute('innerHTML')

#print(driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[2540]').get_attribute('innerText'))
strdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/span').get_attribute('innerHTML')
strprice = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i) + ']/td[4]/span').get_attribute('innerHTML')
while i > 0:
    if i > 1:
        eles = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr['+ str(i - 1) + ']').get_attribute('innerText')
        if "Dividend" in eles:
            nxtdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i - 2) + ']/td[1]/span').get_attribute('innerHTML')
            nxtprice = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i - 2) + ']/td[4]/span').get_attribute('innerHTML')
        elif "Stock Split" in eles:
            strdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i - 2) + ']/td[1]/span').get_attribute('innerHTML')
            strprice = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i - 2) + ']/td[4]/span').get_attribute('innerHTML')
        else:
             nxtdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i - 1) + ']/td[1]/span').get_attribute('innerHTML')
             nxtprice = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i - 1) + ']/td[4]/span').get_attribute('innerHTML')
        
        chng1 = float(nxtprice) - float(strprice)
        chng = chng1 / float(strprice) * 100

        #print(chng)

        if trade == True:
            if chng >= 30:
                trade = False
                print('TUR ended trade ' + nxtdate + " " + nxtprice + " Yes")
            if chng <= -15:
                trade = False
                print('TUR ended trade ' + nxtdate + " " + nxtprice + " No")
        if trade == False:
            if chng >= 15:
                strdate = nxtdate
                strprice = nxtprice
            if chng <= -40:
                print('TUR started trade ' + nxtdate + " " + nxtprice)
                trade = True
                strdate = nxtdate
                strprice = nxtprice
        i = i -1

driver.quit
