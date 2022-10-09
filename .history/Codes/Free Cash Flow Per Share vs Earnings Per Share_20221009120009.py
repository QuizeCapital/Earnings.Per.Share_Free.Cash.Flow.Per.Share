import sys 
path = "/Users/adamszequi/Desktop/Clones/UniversalModules"
sys.path.append(path)
from ExternalModules import modulesSmartFactor
import pandas as pd
import numpy as np
from pprint import pprint
from tabulate import tabulate

class freecashflowpershareByEarnningspershare:
    
    def __init__(self, returnsData, epsData, freeCashFlowPerShareData):
        self.returnsData = returnsData
        self.epsData = epsData
        self.freeCashFlowPerShareData = freeCashFlowPerShareData

    '''
    This function calculates the average return of our universe of 
    about 3000 equities
    It takes our log return dataset from our global variables 
    Returns average of our universe 
    '''
    def universeAvgReturns(self):
        #expand our list of dict of log returns 
        #get values and calculate the mean of those values 
        return (np.nanmean([values for item in modulesSmartFactor().openJson(self.returnsData) for key, values in item.items()]))*100
        
    '''
    This function returns the percentage change of earnings per share of our stock universe 
    It takes the earnings per share data as an undeclared input 
    
    '''
    def epsPctChange(self):
        
        epsDf = (pd.DataFrame(
            [[key, keySub, valueSub] for item in modulesSmartFactor().openJson(self.epsData) for key, value in item.items() for keySub, valueSub in value.items()], columns=["Symbol", "Date", "Earnings Per Share"]  
            )).sort_values(["Symbol","Date"], ascending=[True, True])
        epsDf['EPS Pct Change (2019-2020)'] = (epsDf.groupby("Symbol")["Earnings Per Share"].apply(pd.Series.pct_change) * 100)
        
        return epsDf.dropna()
            
    '''
    This function calculates the percentage change in free cash flow per share 
    of our universe
    It takes a dictionary of symbol, date and free cash flow per share as inputs
    It returns a dataframe of symbol, date (most recent date), free cash flow per share
    of that date, percentage change of free cash flow per share 
    ''' 
    def fcfpsPctChange(self):
        
        fcfpsDf = pd.DataFrame(
            [[key, keySub, valueSub] for item in modulesSmartFactor().openJson(self.freeCashFlowPerShareData) for key, value in item.items() for keySub, valueSub in value.items()], columns=["Symbol", "Date", "Free Cash Flow Per Share"] 
            ).sort_values(["Symbol","Date"], ascending=[True, True])
        fcfpsDf['FCFPS Pct Change (2019-2020)'] = (fcfpsDf.groupby("Symbol")["Free Cash Flow Per Share"].apply(pd.Series.pct_change) * 100)
        
        return fcfpsDf.dropna()
    
        
    
    '''
     This function creates merged 5 quintiles containing intersection of securities
     based in their eps and free cash flow per share
     It takes dataframe of free cash flow and eps as parameter
     It returns a 5by5 array of numbers with free cash flow per share as the vertical area and earnings
     per share as the horizontal area.The values of the array are the mean of returns calculated for each quintile
     based on the intersection of earnings per share and free cash flow per share for that 
     quintile

    '''
    def FCFPSbyEps(self):
            # '''
            # This function splits a list into inputted chunks where we can use that as 
            # our quintile output.
            # '''
    
        # def chunks(lst, n):
        # #Yield successive n-sized chunks from lst.
        #     for i in range(0, len(lst), n):
        #         yield lst[i:i + n]
        
        '''
        This function creates merged 5 quintiles containing intersection of securites
        based in their eps and free cash flow per share
        It takes dataframe of free cash flow and eps as parameter
        It returns a dict of number (descending percentage change) as key and list of tickers for that quinitle as value
        
        '''
        
        def arrayOfFCFPSbyEps(self):
            
            freeCashFlowData = (
                self.fcfpsPctChange()
                .sort_values(['FCFPS Pct Change (2019-2020)'], ascending=[False])
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
            )
            
            quinitileSplitFreeCashFlow = [list(dataframe['Symbol']) for dataframe in [df[['Symbol', 'FCFPS Pct Change (2019-2020)' ]] for df in np.array_split(freeCashFlowData, 25)]]
            
            epsData = (
                self.epsPctChange()
                .sort_values(['EPS Pct Change (2019-2020)'], ascending=[False])
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
            )
            quintileSplitEps = [list(dataframe['Symbol']) for dataframe in [df[['Symbol', 'EPS Pct Change (2019-2020)' ]] for df in np.array_split(epsData, 25)]]

            mergedQuintiles = [[_, values] for _ in range(len(quinitileSplitFreeCashFlow)) for values in quinitileSplitFreeCashFlow[_] if values in quintileSplitEps[_]]
        
            historicalReturnsTickerDict = [
                [lists[0], dictReturnValue]
                for lists in mergedQuintiles
                for values in modulesSmartFactor().openJson(self.returnsData)
                for dictReturnKey,dictReturnValue in  values.items()
                if dictReturnKey in lists
                ]
            lst = list((pd.DataFrame(historicalReturnsTickerDict, columns=['Quintile', 'Returns']).groupby(['Quintile']).mean())['Returns'])
            out =[ lst[i:i + 5] for i in range(0, len(lst), 5)]
            
            return out
        #list((pd.DataFrame(historicalReturnsTickerDict, columns=['Quintile', 'Returns']).groupby(['Quintile']).mean())['Returns'])           
        return arrayOfFCFPSbyEps(self)

pd.set_option('display.max_colwidth', None)
output =   freecashflowpershareByEarnningspershare(
    '/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Earnings Per Share By Free Cash Flow (Excess Returns)/Data/Log Returns Data.json'
    ,'/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Earnings Per Share By Free Cash Flow (Excess Returns)/Data/epsData.json'
    #,'/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Earrnings Per Share By Free Cash Flow (Excess Returns)/Data/Free Cashflow Per Share Data.json'
    ,'/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Earnings Per Share By Free Cash Flow (Excess Returns)/Data/Free Cashflow Per Share Data.json'
)
outputObject =  output.FCFPSbyEps()
print((pd.DataFrame(outputObject),columns=['Quntile 1', 'Quntile 2','Quntile 3','Quntile 4','Quntile 5']))

# plt.plot(outputObject)
# plt.show()