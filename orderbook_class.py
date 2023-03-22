# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:44:59 2020

@author: Maciej Legosz
"""



import pandas as pd
import numpy as np
import time
pd.options.display.max_columns = None
from tabulate import tabulate
import os

class OrderBook(object):
    columns = ['Order ID', 'Order_type', 'Security', 'Direction', 'Size', 
               'Price_limit', 'Status', 'Arrival_time']
    
    def __init__(self, security = 'AMZN'):
        self.security = security
        self.bid_side = {}
        self.ask_side = {}
    
    def get_security(self):
        return self.security
    
    def insert_order(self, order):
        order_id = order.get_order_id()
        order_direction = order.get_direction()
        if order_direction == 'Sell':
            if order_id not in self.ask_side.keys():
                self.ask_side[order_id] = order
            else:
                raise Exception('Order already in the orderbook.')
        else:
            if order_id not in self.bid_side.keys():
                self.bid_side[order_id] = order
            else:
                raise Exception('Order already in the orderbook.')
    
    def pop_order(self, order_id = None):
        if order_id in self.bid_side.keys():
            return self.bid_side.pop(order_id)
        else:
            return self.ask_side.pop(order_id)
                
        
    def to_dataframe(self, bid_side = True):
        book_side = self.bid_side if bid_side else self.ask_side
        order_series = [order.to_series() for order in book_side.values()]
        return pd.concat(objs = order_series, axis = 1).transpose().set_index(keys = 'Order ID')
            
    def sort_price_time(self, bid_side = True):
        """
        Price-Time Precedence sort of the order book side, without order aggregation. 
        Returns a dataframe with the BEST BID or ASK AT THE TOP of the dataframe.
        """
        # book_side = self.bid_side if bid_side else self.ask_side
        if bid_side:
            return self.to_dataframe(bid_side = bid_side).sort_values(axis = 0, 
                                  by = ['Price_limit', 'Arrival_time'],
                                  ascending = [False, True])
        else:
            return self.to_dataframe(bid_side = bid_side).sort_values(axis = 0, 
                                  by = ['Price_limit', 'Arrival_time'],
                                  ascending = [True, True])
    
    def get_aggragate_size(self, bid_side = True):
        
        if bid_side:
            return self.to_dataframe(bid_side = bid_side)['Size'].sum(axis = 0)
        else:
            return self.to_dataframe(bid_side = bid_side)['Size'].sum(axis = 0)
        
        
    def display(self, display_size = 5):
        """
        Displays the current state of the entire order book, i.e. ask side and
        bid side. Needs to be adjusted to show only aggregated orders at a given price.

        Returns
        -------
        None.

        """
        display_columns = ['Security', 'Direction', 'Price_limit', 'Size',
                           'Aggregate_size', 'Arrival_time']
        book_ask_side = self.to_dataframe(bid_side = False)
        book_bid_side = self.to_dataframe(bid_side = True)

        # book_ask_side.set_index(keys = ['Order ID'])
        # book_bid_side.set_index(keys = ['Order ID'])
        
        book_ask_side.sort_values(axis = 0, by = ['Price_limit', 'Arrival_time'],
                                  ascending = [False, False], inplace = True)
        book_bid_side.sort_values(axis = 0, by = ['Price_limit', 'Arrival_time'],
                                  ascending = [False, True], inplace = True)
        
        book_ask_side['Aggregate_size'] = book_ask_side['Size'][::-1].cumsum(axis = 0)[::-1]
        book_bid_side['Aggregate_size'] = book_bid_side['Size'].cumsum(axis = 0)
        
        os.system('cls')
        sep_series = pd.Series(data = [' ' for _ in range(len(book_ask_side.columns))], 
                               index = book_ask_side.columns, name = '')
        
        sep_frame = sep_series.to_frame().transpose()
        
        entire_book = pd.concat([book_ask_side.iloc[-display_size:], sep_frame, 
                                 book_bid_side.iloc[:display_size]]).rename_axis(index = 'Order ID')
        print('\n')
        # print(entire_book)
        print(tabulate(entire_book[display_columns], headers = display_columns,
                        tablefmt = 'fancy_grid', stralign = 'center'))
    
     
if __name__ == '__main__':
    import order_class
    T = 10**(-6)    
    m1 = order_class.MarketOrder(direction = 'Sell', size = 3000, security = "AMZN")    
    lb1 = order_class.LimitOrder(direction = 'Buy', size = 500, price_limit = 1600, security = "AMZN")
    time.sleep(T)
    lb2 = order_class.LimitOrder(direction = 'Buy', size = 100, price_limit = 1700, security = "AMZN")
    time.sleep(T)
    lb3 = order_class.LimitOrder(direction = 'Buy', size = 3000, price_limit = 1750, security = "AMZN")
    time.sleep(T)
    lb4 = order_class.LimitOrder(direction = 'Buy', size = 1500, price_limit = 1750, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    ls1 = order_class.LimitOrder(direction = 'Sell', size = 1500, price_limit = 2000, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    ls2 = order_class.LimitOrder(direction = 'Sell', size = 10000, price_limit = 1800, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    ls3 = order_class.LimitOrder(direction = 'Sell', size = 70, price_limit = 1800, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    ls4 = order_class.LimitOrder(direction = 'Sell', size = 900, price_limit = 1760, security = "AMZN")
    book = OrderBook()
    for i in [lb1, lb2, lb3, lb4, ls1, ls2, ls3, ls4]:
        book.insert_order(i)
    book.display()