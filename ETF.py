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
listE =['TUR','EGPT', 'EWZ', 'EWJ', 'EWY', 'EWG', 'EWA', 'EWC', 'EWH', 'EWT', 'EPOL', 'EWP', 'GREK', 'EZA', 'EWK', 'VNM', 'CYNA']
driver = webdriver.Chrome('C:\Python27\chromedriver.exe')
wait = WebDriverWait(driver, 20)
file = open("trades.txt","w")

def stabalize(nxt, i):
    stchng = float(nxt) * .05
    x = i - 1
    stprice = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(x) + ']/td[4]/span').get_attribute('innerHTML')
    while x > x - 5:
        if float(strprice) < nxt - stchng:
            return "Not Stable"
        elif float(strprice) > nxt + stchng:
            return "Not Stable"
        x = x - 1
        stprice = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(x) + ']/td[4]/span').get_attribute('innerHTML')
        stdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(x) + ']/td[1]/span').get_attribute('innerHTML')    
    return stdate + " " + stprice

def etftrade(etf):
    driver.get("https://finance.yahoo.com/quote/" + etf + "/history?period1=1206680400&period2=1546063200&interval=1d&filter=history&frequency=1d")
    ele = driver.find_element_by_css_selector('tr.Fz\(s\):nth-child(1)')
    wait.until(EC.visibility_of(ele))
    eles = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr')
    i = len(eles)
    getdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/span').get_attribute('innerHTML')
    y = 40000
    oldi = 0
    newi= 1
    trade = False
    newgetdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i - 2) + ']/td[1]/span').get_attribute('innerHTML')
    while oldi != newi:
        oldi = len(eles)
        #print(oldi)
        #getdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/span').get_attribute('innerHTML')
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        time.sleep(2)
        eles = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr')
        newi = len(eles)
        y = y + 40000
        #print(newi)
        #newgetdate = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/span').get_attribute('innerHTML')
    i = len(eles)
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
                    traded = etf + ' ended trade ' + nxtdate + " " + nxtprice + " Yes"
                    print(traded)
                    #file = open("trades.txt","w")
                    file.write(traded + "\n")
                    #file.close
                if chng <= -15:
                    trade = False
                    traded = etf + ' ended trade ' + nxtdate + " " + nxtprice + " No"
                    print(traded)
                    #file = open("trades.txt","w")
                    file.write(traded + "\n")
                   #file.close
            if trade == False:
                if chng >= 15:
                    strdate = nxtdate
                    strprice = nxtprice
                if chng <= -40:
                    st = stabalize(nxtprice, i)
                    if st != "Not Stable":
                        traded = etf + ' started trade ' + st
                        print(traded)
                        #file = open("trades.txt","w")
                        file.write(traded + "\n")
                        #file.close
                        trade = True
                        dateprice = st.split()
                        strdate = dateprice[1] + " " + dateprice[2] + " " + dateprice[3]
                        strprice = dateprice[4]
        i = i -1

for e in listE:
    etftrade(e)
file.close
driver.quit
