import sys 
path = "/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Universal Models"
path = "/Users/adamszequi/Desktop/Clones/UniversalModules"
sys.path.append(path)
from ExternalModules import modulesSmartFactor
from urllib.request import urlopen
import certifi
import json
from dateutil.parser import isoparse
from operator import itemgetter
import pandas as pd
import numpy as np

'''
Junior Datasets codes for this SubProject
'''
class Datasets:
    '''
    setting our variables
    '''
    def __init__(self, epsDataDump, tickerData, freeCashFlowDataDump, logReturnsData, freeCashflowPerShareData, surprise):
        #this is where we dump our earnings per share datasets
        self.epsDataDump = epsDataDump
        #this is where we get our tickers
        self.tickerData = tickerData
        #this is where we dump our free cash flow dataDictList
        self.freeCashFlowDataDump = freeCashFlowDataDump
        #this is where we store or logarithmic returns data
        self.logReturnsData = logReturnsData
        
        self.freeCashflowPerShareData = freeCashflowPerShareData
        
        self.surprise = surprise
    '''
    This functions siphons raw datasets from financial modelling prep
    mainly historical price, eps and free cash flow 
    
    Takes global attributes of class and out puts a json file with cleaned datasets for each 
    subfunction containing either fundamnetal item
    
    
    '''   
    def getCleanedDatasets(self):
                #empty list  to append the  diicts
            # #of symbol, date and revenue per share
            #for loop data that we siphon into
        dataDictList = []
        '''
        This function connects to financial modelling prep's Api
        and gets eps data from the income statement section 
        as bulk data 
        Takes original ticker data as parameter and returns 
        returns each tickers data with limit of 7 years
        '''

        def getCleanedEpsData(self):  # sourcery skip: avoid-builtin-shadow
            for count, ticker in enumerate(modulesSmartFactor().openCsv(self.tickerData)['Ticker'], start=1):
                
                #Api connection with 7 year limit 
                #and feeding in the ticker name
                url = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=7&apikey=764a0c82850f17c8235116b78792d7e1'
                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")

                if  bulkData := json.loads(data):
                    #bulk income statement data 
                    dict = bulkData
            # #connect to getdatafrom API function
            # #and siphon data indidually into this function
            # connectApi = getDataFromApi(self)
            # #set initial and end dates for specificifty
            # #dealing with portfolios created before or after the
            # #a certain time
                    initialDate = '2021-01-01'
                    finalDate = '2018-12-31'
            
            #compare dates and get value between two dates
                    for dictionaryValue in dict:
                        if isoparse(dictionaryValue.get('date')) > isoparse(finalDate) and isoparse(dictionaryValue.get('date')) < isoparse(initialDate):
                            dictInfo =  {dictionaryValue.get('symbol'): {dictionaryValue.get('date'): dictionaryValue.get('epsdiluted')}}
                            print(count)
                            print(dictInfo)
                            dataDictList.append(dictInfo)
                            #print(dataDictList)

            return modulesSmartFactor().dumpJson(self.epsDataDump, dataDictList)
            
        def getCleanedFreeCashflowData(self):  # sourcery skip: avoid-builtin-shadow
            for count, ticker in enumerate(modulesSmartFactor().openCsv(self.tickerData)['Ticker'], start=1):
                
                #Api connection with 7 year limit 
                #and feeding in the ticker name
                url = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=7&apikey=764a0c82850f17c8235116b78792d7e1'
                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")

                if  bulkData := json.loads(data):
                    #bulk income statement data 
                    dict = bulkData
            # #connect to getdatafrom API function
            # #and siphon data indidually into this function
            # connectApi = getDataFromApi(self)
            # #set initial and end dates for specificifty
            # #dealing with portfolios created before or after the
            # #a certain time
                    initialDate = '2021-01-01'
                    finalDate = '2018-12-31'
            
            #compare dates and get value between two dates
                    for dictionaryValue in dict:
                        if isoparse(dictionaryValue.get('date')) > isoparse(finalDate) and isoparse(dictionaryValue.get('date')) < isoparse(initialDate):
                            dictInfo =  {dictionaryValue.get('symbol'): {dictionaryValue.get('date'): dictionaryValue.get('freeCashFlow')}}
                            print(count)
                            print(dictInfo)
                            dataDictList.append(dictInfo)
                            #print(dataDictList)

            return modulesSmartFactor().dumpJson(self.freeCashFlowDataDump, dataDictList)
        
        def getCleanedHistoricalPriceData(self):
            #initialise a list with dict
            #of annualised logreturns
            dictReturns = []
            # sourcery skip: avoid-builtin-shadow
            for count, ticker in enumerate(modulesSmartFactor().openCsv(self.tickerData)['Ticker'], start=1):
                #Api connection wfor historical data for 2021
                url = f'https://financialmodelingprep.com//api/v3/historical-price-full/{ticker}?from=2021-01-01&to=2021-12-31&apikey=764a0c82850f17c8235116b78792d7e1'
                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")
                if  bulkData := json.loads(data):
                    #bulk price data
                    dict = bulkData
                    #get adjusted close data from 
                    #historical data 
                    priceInfoBulk = list((map(itemgetter('adjClose'),dict.get('historical', {}))))
                    #get dymbol attached to adjusted close
                    symbol = (dict.get('symbol', {}))
                    #flip adjusted close data 
                    #becuase years start from closest year 
                    priceDf = pd.Series(priceInfoBulk).iloc[::-1]
                    #calculate logarithmic annual return
                    logRet = (np.log(priceDf) - np.log(priceDf.shift(1))).sum()
                    epsData = {symbol: logRet}
                    print(count)
                    print(epsData)
                    dictReturns.append(epsData)
             #dump data into returns json file by 
             #calling dumpjson attribute in modules file       
            return modulesSmartFactor().dumpJson(self.logReturnsData , dictReturns)   
        
        def getCleanedFreeCashflowPerShareData(self):  # sourcery skip: avoid-builtin-shadow
            for count, ticker in enumerate(modulesSmartFactor().openCsv(self.tickerData)['Ticker'], start=1):
                
                #Api connection with 7 year limit 
                #and feeding in the ticker name
                url = f'https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?limit=7&apikey=764a0c82850f17c8235116b78792d7e1'
                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")

                if  bulkData := json.loads(data):
                    #bulk income statement data 
                    dict = bulkData
                     
            # #connect to getdatafrom API function
            # #and siphon data indidually into this function
            # connectApi = getDataFromApi(self)
            # #set initial and end dates for specificifty
            # #dealing with portfolios created before or after the
            # #a certain time
                    initialDate = '2021-01-01'
                    finalDate = '2018-12-31'
            
            #compare dates and get value between two dates
                    for dictionaryValue in dict:
                        if isoparse(dictionaryValue.get('date')) > isoparse(finalDate) and isoparse(dictionaryValue.get('date')) < isoparse(initialDate):
                            dictInfo =  {dictionaryValue.get('symbol'): {dictionaryValue.get('date'): dictionaryValue.get('freeCashFlowPerShare')}}
                            print(count)
                            print(dictInfo)
                            dataDictList.append(dictInfo)
                            #print(dataDictList)

            return modulesSmartFactor().dumpJson(self.freeCashflowPerShareData, dataDictList)   

        def Surprise(self):  # sourcery skip: avoid-builtin-shadow
            for count, ticker in enumerate(modulesSmartFactor().openCsv(self.tickerData)['Ticker'], start=1):
                
                #Api connection with 7 year limit 
                #and feeding in the ticker name
                url = f'https://financialmodelingprep.com/api/v3/earnings-surprises/{ticker}?limit=7&apikey=764a0c82850f17c8235116b78792d7e1'
                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")

                if  bulkData := json.loads(data):
                    #bulk income statement data 
                    dict = bulkData
                     
            # #connect to getdatafrom API function
            # #and siphon data indidually into this function
            # connectApi = getDataFromApi(self)
            # #set initial and end dates for specificifty
            # #dealing with portfolios created before or after the
            # #a certain time
                    initialDate = '2021-01-01'
                    finalDate = '2018-12-31'
            
            #compare dates and get value between two dates
                    # for dictionaryValue in dict:
                        # if isoparse(dictionaryValue.get('date')) > isoparse(finalDate) and isoparse(dictionaryValue.get('date')) < isoparse(initialDate):
                            # dictInfo =  {dictionaryValue.get('symbol'): {dictionaryValue.get('date'): dictionaryValue.get('freeCashFlowPerShare')}}
                    print(count)
                    print(dict)
                    dataDictList.append(dict)
                            #print(dataDictList)

            return modulesSmartFactor().dumpJson(self.surprise, dataDictList) 
        
        return Surprise(self)
        

outPut = Datasets(
    "/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/earningsPerShareBYfreeCashFlowBasedOnReturns/Data/epsData.json"
    ,"/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Master Dataset File/marketCapDataCleaned.csv"
    ,"/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/earningsPerShareBYfreeCashFlowBasedOnReturns/Data/free cashflow data.json"
    ,"/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/earningsPerShareBYfreeCashFlowBasedOnReturns/Data/Log Returns Data.json"
    ,"/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Earrnings Per Share By Free Cash Flow (Excess Returns)/Data/Free Cashflow Per Share Data.json"
    ,"/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Earrnings Per Share By Free Cash Flow (Excess Returns)/Data/1earningssurprise_actualearn.json"
)    
(outPut.getCleanedDatasets())
            
        
# print((modulesSmartFactor().openCsv("/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Master Dataset File/marketCapDataCleaned.csv")).columns)