from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os
from time import sleep
import datetime
import ibm_db

dsn_hostname = ""
dsn_uid = ""
dsn_pwd = ""
dsn_driver = ""
dsn_database = ""
dsn_port = ""
dsn_protocol = ""
dsn_security = ""
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname,
                            dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)
conn = ibm_db.connect(dsn, "", "")


def create_tables():
    ibm_db.exec_immediate(conn, "create table sber_1 ("
                                "data_day date not null,"
                                "data_hours decimal(2,0) not null,"
                                "sell_dollar decimal(4,2) not null,"
                                "buy_dollar decimal(4,2) not null,"
                                "sell_euro decimal(4,2) not null,"
                                "buy_euro decimal(4,2) not null);")
    ibm_db.exec_immeadite(conn, "create table sber_550 ("
                                "data_day date not null,"
                                "data_hours decimal(2,0) not null,"
                                "sell_dollar decimal(4,2) not null,"
                                "buy_dollar decimal(4,2) not null,"
                                "sell_euro decimal(4,2) not null,"
                                "buy_euro decimal(4,2) not null);")
    ibm_db.exec_immeadite(conn, "create table sber_1500 ("
                                "data_day date not null,"
                                "data_hours decimal(2,0) not null,"
                                "sell_dollar decimal(4,2) not null,"
                                "buy_dollar decimal(4,2) not null,"
                                "sell_euro decimal(4,2) not null,"
                                "buy_euro decimal(4,2) not null);")
    ibm_db.exec_immeadite(conn, "create table sber_15000 ("
                                "data_day date not null,"
                                "data_hours decimal(2,0) not null,"
                                "sell_dollar decimal(4,2) not null,"
                                "buy_dollar decimal(4,2) not null,"
                                "sell_euro decimal(4,2) not null,"
                                "buy_euro decimal(4,2) not null);")
    ibm_db.exec_immeadite(conn, "create table raifa ("
                                "data_day date not null,"
                                "data_hours decimal(2,0) not null,"
                                "sell_dollar decimal(4,2) not null,"
                                "buy_dollar decimal(4,2) not null,"
                                "sell_euro decimal(4,2) not null,"
                                "buy_euro decimal(4,2) not null);")
    ibm_db.exec_immeadite(conn, "create table alpha ("
                                "data_day date not null,"
                                "data_hours decimal(2,0) not null,"
                                "sell_dollar decimal(4,2) not null,"
                                "buy_dollar decimal(4,2) not null,"
                                "sell_euro decimal(4,2) not null,"
                                "buy_euro decimal(4,2) not null);")
    ibm_db.exec_immeadite(conn, "create table tinkoff ("
                                "data_day date not null,"
                                "data_hours decimal(2,0) not null,"
                                "sell_dollar decimal(4,2) not null,"
                                "buy_dollar decimal(4,2) not null,"
                                "sell_euro decimal(4,2) not null,"
                                "buy_euro decimal(4,2) not null);")
    ibm_db.exec_immeadite(conn, "create table vtb_1 ("
                                "data_day date not null,"
                                "data_hours decimal(2,0) not null,"
                                "sell_dollar decimal(4,2) not null,"
                                "buy_dollar decimal(4,2) not null,"
                                "sell_euro decimal(4,2) not null,"
                                "buy_euro decimal(4,2) not null);")
    ibm_db.exec_immeadite(conn, "create table vtb_30000 ("
                                "data_day date not null,"
                                "data_hours decimal(2,0) not null,"
                                "sell_dollar decimal(4,2) not null,"
                                "buy_dollar decimal(4,2) not null,"
                                "sell_euro decimal(4,2) not null,"
                                "buy_euro decimal(4,2) not null);")


def information_raif():
    url = 'https://www.raiffeisen.ru/currency_rates/'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.169'
                      ' Yowser/2.5 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    values = soup.find_all(class_='b-table__td')
    dollar_sell = values[9].text.strip()[:-2]
    euro_sell = values[14].text.strip()[:-2]
    dollar_buy = values[8].text.strip()[:-2]
    euro_buy = values[13].text.strip()[:-2]
    data_day, data_time = str(datetime.datetime.now()).split()
    data_time = int(data_time[:2])
    ibm_db.exec_immediate(conn, f"INSERT INTO RAIFA VALUES ({data_day}, {data_time}, {dollar_sell}, "
                                f"{dollar_buy}, {euro_sell}, {euro_buy});")


def information_tinkoff():
    driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'))
    url = 'https://www.tinkoff.ru/about/exchange/'
    driver.get(url)
    sleep(0.4)
    values = driver.find_elements_by_class_name('a1daNl')

    euro_sell = values[1].text
    euro_buy = values[2].text
    print(euro_sell, euro_buy)
    sleep(0.4)

    driver.find_elements_by_class_name('f2hNHA')[1].click()
    sleep(0.4)
    driver.find_elements_by_class_name('l2RhOB')[2].click()
    sleep(0.4)
    values = driver.find_elements_by_class_name('a1daNl')
    dollar_sell = values[1].text
    dollar_buy = values[2].text
    driver.close()
    data_day, data_time = str(datetime.datetime.now()).split()
    data_time = int(data_time[:2])
    ibm_db.exec_immediate(conn, f"INSERT INTO TINKOFF VALUES ({data_day}, {data_time}, {dollar_sell}, "
                                f"{dollar_buy}, {euro_sell}, {euro_buy});")


def information_alpha():
    driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'))
    url = 'https://alfabank.ru/currency/'
    driver.get(url)
    sleep(0.6)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    values = soup.find_all(class_='a2swtV x2swtV e23Qzr Q23Qzr')
    euro_sell = values[4].text.strip()[:-2]
    euro_buy = values[5].text.strip()[:-2]
    print(euro_sell, euro_buy)
    sleep(0.2)
    button = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div/div/div/div/div[1]/div[1]/button[2]')[0]
    driver.execute_script('arguments[0].click();', button)
    sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    values = soup.find_all(class_='a2swtV x2swtV e23Qzr Q23Qzr')
    dollar_sell = values[4].text.strip()[:-2]
    dollar_buy = values[5].text.strip()[:-2]
    driver.close()
    data_day, data_time = str(datetime.datetime.now()).split()
    data_time = int(data_time[:2])
    ibm_db.exec_immediate(conn, f"INSERT INTO ALPHA VALUES ({data_day}, {data_time}, {dollar_sell}, "
                                f"{dollar_buy}, {euro_sell}, {euro_buy});")


def information_vtb():
    driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'))
    url = 'https://www.vtb.ru/personal/platezhi-i-perevody/obmen-valjuty/'
    driver.get(url)
    sleep(0.2)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    values = soup.find_all(class_='exchange-rate-table__index ng-binding ng-scope exchange-rate-table__index_up')
    dollar_1_sell = values[1].text.strip()
    dollar_1_buy = values[0].text.strip()
    euro_1_sell = values[3].text.strip()
    euro_1_buy = values[2].text.strip()
    button_dollar = driver.find_element_by_xpath(
        '/html/body/main/div/section[5]/div/div/div/div[2]/div/div[1]/div/section[1]/'
        'div[2]/div/div[1]/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/'
        'td[1]/div[2]/a[2]')
    driver.execute_script('arguments[0].click();', button_dollar)
    sleep(0.4)
    button_euro = driver.find_element_by_xpath(
        '/html/body/main/div/section[5]/div/div/div/div[2]/div/div[1]/div/section[1]'
        '/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/table/tbody/'
        'tr[3]/td[1]/div[2]/a[2]')

    driver.execute_script('arguments[0].click();', button_euro)
    sleep(0.4)
    dollar_30000_sell = driver.find_element_by_xpath('/html/body/main/div/section[5]/div/div/div/div[2]/div/div[1]/'
                                                     'div/section[1]/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/'
                                                     'table/tbody/tr[2]/td[3]/div/span').text

    dollar_30000_buy = driver.find_element_by_xpath('/html/body/main/div/section[5]/div/div/div/div[2]/div/div[1]/div/'
                                                    'section[1]/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/'
                                                    'table/tbody/tr[2]/td[2]/div/span').text
    euro_30000_sell = driver.find_element_by_xpath('/html/body/main/div/section[5]/div/div/div/div[2]/div/div[1]/div/'
                                                   'section[1]/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/table/tbody'
                                                   '/tr[3]/td[3]/div/span').text
    euro_30000_buy = driver.find_element_by_xpath('/html/body/main/div/section[5]/div/div/div/div[2]/div/div[1]/div/'
                                                  'section[1]/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/table/'
                                                  'tbody/tr[3]/td[2]/div/span').text
    driver.close()
    data_day, data_time = str(datetime.datetime.now()).split()
    data_time = int(data_time[:2])
    ibm_db.exec_immediate(conn, f"INSERT INTO VTB_1 VALUES ({data_day}, {data_time}, {dollar_1_sell}, "
                                f"{dollar_1_buy}, {euro_1_sell}, {euro_1_buy});")
    ibm_db.exec_immediate(conn, f"INSERT INTO VTB_30000 VALUES ({data_day}, {data_time}, {dollar_30000_sell}, "
                                f"{dollar_30000_buy}, {euro_30000_sell}, {euro_30000_buy});")