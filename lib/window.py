import ibm_db
import ibm_db_dbi
from kivy.lang import Builder
from kivymd.app import MDApp
import matplotlib.pyplot as plt
from datetime import datetime
from kivy.uix.floatlayout import FloatLayout
import matplotlib
from kivy.core.window import Window

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


class Settings(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_graphic(self, type, currency, sber, vtb):
        conn = ibm_db.connect(dsn, "", "")
        pconn = ibm_db_dbi.Connection(conn)
        cur = pconn.cursor()
        cur.execute("SELECT data_day,data_hours from raifa")
        data = cur.fetchall()
        new_data = []
        for i in data:
            new_data.append(f'{str(i[0])} {i[1]}')
        data_for_table = matplotlib.dates.date2num(
            [datetime.strptime(one_data, '%Y-%m-%d %H') for one_data in new_data])
        formatter = matplotlib.dates.DateFormatter('%d/%H')
        figure = plt.figure(figsize=(16, 9))
        axes = figure.add_subplot(1, 1, 1)
        axes.xaxis.set_major_formatter(formatter)
        plt.setp(axes.get_xticklabels(), rotation=15)
        cur.execute(f"SELECT {type}_{currency} from tinkoff;")
        tinkoff_buy_dollar = cur.fetchall()
        tinkoff_buy_dollar = list(map(lambda x: float(x[0]), tinkoff_buy_dollar))

        cur.execute(f"SELECT {type}_{currency} from raifa")
        raif_buy_dollar = cur.fetchall()
        raif_buy_dollar = list(map(lambda x: float(x[0]), raif_buy_dollar))

        cur.execute(f"SELECT {type}_{currency} from alpha")
        alpha_buy_dollar = cur.fetchall()
        alpha_buy_dollar = list(map(lambda x: float(x[0]), alpha_buy_dollar))

        cur.execute(f"SELECT {type}_{currency} from {sber}")
        sber_buy_dollar = cur.fetchall()
        sber_buy_dollar = list(map(lambda x: float(x[0]), sber_buy_dollar))

        cur.execute(f"SELECT {type}_{currency} from {vtb}")
        vtb_buy_dollar = cur.fetchall()
        vtb_buy_dollar = list(map(lambda x: float(x[0]), vtb_buy_dollar))

        axes.plot(
            data_for_table,
            tinkoff_buy_dollar,
            color='black',
            linewidth=2,
            label='Tinkoff Bank')
        axes.plot(
            data_for_table,
            raif_buy_dollar,
            color='yellow',
            linewidth=2,
            label='Raiffeisen Bank'
        )
        axes.plot(
            data_for_table,
            alpha_buy_dollar,
            color='red',
            linewidth=2,
            label='AlfaBank'
        )
        axes.plot(
            data_for_table,
            sber_buy_dollar,
            color='green',
            linewidth=2,
            label='SberBank'
        )
        axes.plot(
            data_for_table,
            vtb_buy_dollar,
            color='blue',
            linewidth=2,
            label='VTB Bank'
        )
        plt.legend(
            loc='upper left',
            borderaxespad=5
        )
        plt.xlabel('Day and hours')
        plt.ylabel('Price')
        plt.show()
        pconn.close()


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_file("lib/settings.kv")
        return Settings()


Window.size = (1000, 600)
