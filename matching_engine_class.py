# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:13:33 2020

@author: Maciej Legosz
"""
import pandas as pd
import order_class
import orderbook_class
import datetime as dt

class MatchingEnging(object):
    
    def __init__(self, orderbook, price_history_db):
        self.orderbook = orderbook
        self.price_history_db = price_history_db
        self.fifo_buffer = []
    
    def add_to_buffer(self, order):
        self.fifo_buffer.append[order]
        
    def remove_from_buffer(self):
        self.fifo_buffer.pop(index = 0)
        
    def get_best_buy_order(self):
        sorted_bid_side = self.orderbook.sort_price_time(bid_side = True)
        best_buy_order_id = sorted_bid_side.loc[0,'Order ID']
        return self.orderbook[best_buy_order_id]
    
    def get_best_sell_order(self):
        sorted_ask_side = self.orderbook.sort_price_time(bid_side = False)
        best_sell_order_id = sorted_ask_side.loc[0,'Order ID']
        return self.orderbook[best_sell_order_id]
    
    def match_sell_market_order(self, sell_market_order):
        remaining_size = sell_market_order.get_size()
        sorted_bid_side = self.orderbook.sort_price_time(bid_side = True)
        order_counter = 0
        
        while remaining_size > 0:
            buy_order_size = sorted_bid_side['Size'].iloc[order_counter]
            buy_order_id = sorted_bid_side.iloc[order_counter].name
            
            if remaining_size == buy_order_size:
                remaining_size -= buy_order_size
                matched_buy_order = self.orderbook.pop_order(buy_order_id)
                trade_data = [matched_buy_order.get_price_limit(), dt.datetime.now(),
                              [buy_order_id, sell_market_order.get_order_id()],
                              buy_order_size]
                self.price_history_db.insert_trade(trade_data) 
            elif remaining_size > buy_order_size:
                remaining_size -= buy_order_size
                matched_buy_order = self.orderbook.pop_order(buy_order_id)                
                trade_data = [matched_buy_order.get_price_limit(), dt.datetime.now(),
                              [buy_order_id, sell_market_order.get_order_id()],
                              buy_order_size]
                self.price_history_db.insert_trade(trade_data)
                order_counter += 1
            else:
                updated_size = buy_order_size - remaining_size
                self.orderbook.bid_side[buy_order_id].update_size(updated_size = updated_size)
                remaining_size = 0
                
        
    def match_buy_market_order(self, buy_market_order):
        remaining_size = buy_market_order.get_size()
        sorted_ask_side = self.orderbook.sort_price_time(bid_side = False)
        order_counter = 0
        
        while remaining_size > 0:
            sell_order_size = sorted_ask_side['Size'].iloc[order_counter]
            sell_order_id = sorted_ask_side.iloc[order_counter].name
            
            if remaining_size == sell_order_size:
                remaining_size -= sell_order_size
                matched_sell_order = self.orderbook.pop_order(sell_order_id)
                trade_data = [matched_sell_order.get_price_limit(), dt.datetime.now(),
                              [sell_order_id, buy_market_order.get_order_id()],
                              sell_order_size]
                self.price_history_db.insert_trade(trade_data) 
            elif remaining_size > sell_order_size:
                remaining_size -= sell_order_size
                matched_sell_order = self.orderbook.pop_order(sell_order_id)                
                trade_data = [matched_sell_order.get_price_limit(), dt.datetime.now(),
                              [sell_order_id, buy_market_order.get_order_id()],
                              sell_order_size]
                self.price_history_db.insert_trade(trade_data)
                order_counter += 1
            else:
                updated_size = sell_order_size - remaining_size
                self.orderbook.ask_side[sell_order_id].update_size(updated_size = updated_size)
                remaining_size = 0
    
    def route_order(self, order):
        order_type = order.get_order_type()
        direction = order.get_direction()
        if order_type == 'Market':
            self.add_to_buffer(order)
        else:
            price_limit = order.get_price_limit()
            best_buy_price = self.get_best_buy_order().get_price_limit()
            best_sell_price = self.get_best_sell_order().get_price_limit()
            if direction == 'Sell':
                if price_limit > best_buy_price:
                    self.orderbook.insert_order(order)
                else:
                    self.match_sell_limit_order(sell_limit_order = order) # to be implemented
            else: 
                if price_limit < best_sell_price:
                    self.orderbook.insert_order(order)
                else:
                    self.match_buy_limit_order(buy_limit_order = order) # to be implemented
                
    def match_sell_limit_order(self, sell_limit_order):
        pass
        
        
        