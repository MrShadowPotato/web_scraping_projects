from bs4 import BeautifulSoup
import requests
import datetime
import time
from requests_html import HTMLSession


class CurrencyService:
    #This class scrapes the Banco Central web page in order to get UF, USD and EUR prices in CLP in a given date range.
    INITIAL_URL = 'https://si3.bcentral.cl/Bdemovil/BDE/IndicadoresDiarios?parentMenuName=Indicadores%20diarios&fecha='

    @staticmethod
    def __dates_list(initial_date, end_date):
        #Returns a list of dates between the inintial and end dates.
        date_format  = '%d-%m-%Y'
        initial_date = datetime.datetime.strptime(initial_date, date_format)
        end_date = datetime.datetime.strptime(end_date, date_format)
        current_date = initial_date
        date_list = []
        while current_date <= end_date:
            date_list.append(current_date.strftime(date_format))
            current_date += datetime.timedelta(days=1)
        return date_list

    @staticmethod
    def __scrape_web_page(date):
        #Returns a list contaning the prices in CLP for UF, USD and EUR for a given date.
        url = CurrencyService.INITIAL_URL + date
        html_text = requests.get(url).text
        print(html_text)
        soup = BeautifulSoup(html_text, 'html5lib')
        uf = soup.find_all('td', class_='col-xs-2 text-center')[0].text
        usd = soup.find_all('td', class_='col-xs-2 text-center')[1].text
        eur = soup.find_all('td', class_='col-xs-2 text-center')[2].text
        return [uf, usd, eur]


    @staticmethod
    def currencies(initial_date, end_date):
        #Returns a dictionary with the currencies as the keys to access their lists of prices in CLP for a given range.
        currencies = {'uf': [], 'usd': [], 'eur': []}
        dates = CurrencyService.__dates_list(initial_date, end_date)
        for date in dates:
            uf, usd, eur = CurrencyService.__scrape_web_page(date)
            currencies['uf'].append(uf)
            currencies['usd'].append(usd)
            currencies['eur'].append(eur)
            time.sleep(1)
        return currencies

#currencies = CurrencyService.currencies('13-09-2022', '18-09-2022') 
#print(currencies)
        
#x = CurrencyService._CurrencyService__scrape_web_page('14-09-2022')
#print(x)
day_one = 'https://si3.bcentral.cl/Bdemovil/BDE/IndicadoresDiarios?parentMenuName=Indicadores%20diarios&fecha=14-09-2022'
day_two = 'https://si3.bcentral.cl/Bdemovil/BDE/IndicadoresDiarios?parentMenuName=Indicadores%20diarios&fecha=13-09-2022'

session = HTMLSession()
r = session.get(day_one).text
r2 = session.get(day_two).text
print(r == r2)