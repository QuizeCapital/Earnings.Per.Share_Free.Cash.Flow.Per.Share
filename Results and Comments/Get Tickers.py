try:
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import certifi
import json
import pandas as pd
import json

class Project_getTickers():
    
    #def __init__(self):
    
    def get_all_tickers(self):
        tickers_list=[]
        #exchange_list=[]
        #exchange_name=[]
        url = "https://financialmodelingprep.com/api/v3/stock/list?apikey=764a0c82850f17c8235116b78792d7e1"
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        listed_data= json.loads(data)
        for ticks in listed_data:
            stock_abbrev=list(ticks.items())[0][1]
            #exchanges=list(ticks.items())[4][1]
           # exchange_names=list(ticks.items())[3][1]
            #exchange_list.append(exchanges)
            tickers_list. append(stock_abbrev)
            #exchange_name.append(exchange_names)
        return listed_data
    
    def get_market_cap(self,url):
        #url = f"https://financialmodelingprep.com/api/v3/market-capitalization/{ticker}?apikey=764a0c82850f17c8235116b78792d7e1"
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        return json.loads(data)
            
    def get_market_value_dataframe(self):
        count=0
        all_tickers=self.get_all_tickers()
        lists_of_dict_tickers=[]
        for ticker in all_tickers:
            url = f"https://financialmodelingprep.com/api/v3/market-capitalization/{ticker}?apikey=764a0c82850f17c8235116b78792d7e1"
            if tick_list := self.get_market_cap(url):
                lists_of_dict_tickers.append(tick_list[0])
        df= pd.DataFrame(lists_of_dict_tickers)
        #return df.to_csv('/Users/adamszequi/Desktop/Market_cap.csv',mode='a', header=False)
    #@staticmethod
    def open_get_marketCap_data(self,url):
        exchange_list=['Nasdaq Global Market','American Stock Exchange','AMEX','Nasdaq','NASDAQ Global Select''Nasdaq Global Select',
                       'BATS Exchange','NASDAQ','Nasdaq Capital Market',
                       'NASDAQ Global Market','New York Stock Exchange','New York Stock Exchange Arca','NASDAQ Capital Market','NasdaqGS', 
                       'FTSE Index','NYSE American']
        list_of_ticker_data=self.get_all_tickers()
        stock_tickers = [list(ticker.items())[0][1] for ticker in list_of_ticker_data if list(ticker.items())[5][1] == 'stock']
        stock_price = [list(price.items())[0][1] for price in list_of_ticker_data if list(price.items())[2][1] > 2]
        exchange_name=[list(exchange.items())[0][1] for exchange in list_of_ticker_data if list(exchange.items())[3][1] in exchange_list]

        data= pd.read_csv(url,usecols = [0,1,2] ,names=['Ticker','Date','MarketCap'])
        #test_companies = data[(data['MarketCap'] > 500000000) & (data['Ticker'].isin(stock_tickers)) & (data['Ticker'].isin(stock_price)) & (data['Ticker'].isin(exchange_name))]
        test_companies = data[((data['MarketCap'] > 500000000) & (data['Ticker'].isin(stock_tickers)) & (data['Ticker'].isin(stock_price)) & data['Ticker'].isin(exchange_name))]

        below_market = data[(data['MarketCap'] < 500000000)]
        return test_companies
        ##return len(stock_tickers)
        #return len(test_companies)
     
    def markCapScreener_finmod(self,url):
        #url='https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=300000000&country=US&priceMoreThan=2&apikey=764a0c82850f17c8235116b78792d7e1'
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        listed_data= json.loads(data)
        print(len(listed_data))
        
startPoint = Project_getTickers()
#print(startPoint.markCapScreener_finmod\
     # ('https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=500000000&country=US&priceMoreThan=2&apikey=764a0c82850f17c8235116b78792d7e1'))
#print(startPoint.get_all_tickers())
print(startPoint.open_get_marketCap_data('/Users/adamszequi/Desktop/Market_cap.csv').to_markdown())
