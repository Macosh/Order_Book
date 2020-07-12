# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:45:30 2020

@author: Maciej Legosz
"""

import random
import order_class as oc
import orderbook_class as ob
import price_history_db as phdb
import numpy as np
import time

class PrimaryOrderGenerator(object):
    
    indicative_order_count = 1000
    sigma = 0.1
    k = 5
    def __init__(self, empty_orderbook, previous_close_price):
        self.orderbook = empty_orderbook
        self.previous_close_price = previous_close_price
        
    def generate_bid_side(self, order_count = indicative_order_count):
        random_prices = np.round(np.random.normal(loc = self.previous_close_price, 
                                         scale = PrimaryOrderGenerator.sigma * self.previous_close_price, 
                                         size = order_count), decimals = 2)
        random_bid_prices = random_prices[random_prices < self.previous_close_price]
        random_order_sizes = np.random.randint(low = 100, high = 1000, size = len(random_bid_prices))
        time_delay = 10**(-PrimaryOrderGenerator.k)
        for i in range(len(random_bid_prices)):
            self.orderbook.insert_order(oc.LimitOrder(direction = 'Buy', size = random_order_sizes[i],
                                            price_limit = random_bid_prices[i]))
            time.sleep(time_delay)
        
    def generate_ask_side(self, order_count = indicative_order_count):
        random_prices = np.round(np.random.normal(loc = self.previous_close_price, 
                                         scale = PrimaryOrderGenerator.sigma * self.previous_close_price, 
                                         size = order_count), decimals = 2)
        random_ask_prices = random_prices[random_prices > self.previous_close_price]
        random_order_sizes = np.random.randint(low = 100, high = 1000, size = len(random_ask_prices))
        time_delay = 10**(-PrimaryOrderGenerator.k)
        for i in range(len(random_ask_prices)):
            self.orderbook.insert_order(oc.LimitOrder(direction = 'Sell', size = random_order_sizes[i],
                                            price_limit = random_ask_prices[i]))
            time.sleep(time_delay)

class OrderGenerator(object):
    
    def __init__(self, orderbook, price_history_db):
        self.orderbook = orderbook
        self.price_history_db = price_history_db
        self.security = orderbook.get_security()
        self.order_type = ['Market', 'Limit']
        self.order_direction = ['Buy', 'Sell']
        self.order_size = None
    
    
    def get_last_traded_price(self):
        return self.price_history_db.get_last_traded_price()
    
    
    def generate_market_order(self):
        direction = self.order_direction[0] if random.uniform(0,1) <= 0.5 else self.order_direction[1]
        size = 1000
        security = self.security
        return oc.MarketOrder(direction, size, security)
    
    
    def generate_limit_order(self):
        direction = self.order_direction[0] if random.uniform(0,1) <= 0.5 else self.order_direction[1]
        size = 1000
        security = self.security
        mu = self.price_history_db.get_last_traded_price()
        sigma = self.price_history_db.get_total_volume() / self.price_history_db.get_trade_count()
        price_limit = random.normalvariate(mu = mu, sigma = sigma)
        return oc.LimitOrder(direction, size, price_limit, security)
    
    def set_order_type(self):
        return 'Market' if random.uniform(0,1) < 0.5 else 'Limit'
    
    
    
if __name__ == '__main__':

        book = ob.OrderBook()
        primary_generator = PrimaryOrderGenerator(book, previous_close_price = 2230)
        primary_generator.generate_ask_side()
        primary_generator.generate_bid_side()
        book.display_book()
    
        
        
        
    
        