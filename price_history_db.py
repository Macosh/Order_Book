# -*- coding: utf-8 -*-
"""
Created on Tue May  5 20:29:45 2020

@author: Maciej Legosz
"""

import pandas as pd
import numpy as np

class PriceHistoryDB(object):
    
    columns = ['Traded_price', 'Execution_time', 'Matched_orders', 'Size']

    def __init__(self, security = 'AMZN'):
        self.security = security
        self.price_history_db = pd.DataFrame(columns = PriceHistoryDB.columns)
        
    def insert_trade(self, trade_data):
        trade_details = pd.DataFrame(data = np.array(trade_data).reshape((1,4)), columns = PriceHistoryDB.columns)
        self.price_history_db = self.price_history_db.append(other = trade_details,
                                                             ignore_index = True)
        
    def get_last_traded_price(self):
        return self.price_history_db.iloc[-1]['Traded_price']
    
    def get_trade_count(self):
        return self.price_history_db.shape[0]
    
    def get_price_history(self, execution_time_index = True):
        if execution_time_index:
            return self.price_history_db.set_index(keys = ['Execution_time'])['Traded_price']
        else:
            return self.price_history_db['Traded_price']
    
    def get_total_volume(self):
        return self.price_history_db['Size'].sum()
    
    
if __name__ == '__main__':
    db = PriceHistoryDB()
    data = [100, '12:15:01', [25, 54], 2000]
    db.insert_trade(data)
    data = [125, '12:17:25', [4, 21], 4000]
    db.insert_trade(data)
    data = [110, '13:27:00', [11, 10], 5000]
    db.insert_trade(data)
    print(db.get_price_history())            
    
