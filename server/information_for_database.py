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
