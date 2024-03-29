# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 20:56:06 2020

@author: Maciej Legosz
"""
import datetime as dt
import pandas as pd



class Order(object):
    order_id = 0

    def __init__(self, direction: str, size: int, security: str):
        Order.order_id += 1
        self.order_id = Order.order_id
        self.security = security
        self.direction = direction
        self.size = size
        self.status = 'Pending'
        self.arrival_time = dt.datetime.now()
        self.execution_price = None

    def get_order_id(self):
        return self.order_id

    def get_security(self):
        return self.security

    def get_direction(self):
        return self.direction

    def get_size(self):
        return self.size

    def get_status(self):
        return self.status

    def get_arrival_time(self):
        return self.arrival_time

    def update_status(self, new_status: str):
        self.status = new_status

    def update_execution_price(self, execution_price: float):
        self.execution_price = execution_price

    def update_size(self, updated_size: int):
        self.size = updated_size


class MarketOrder(Order):
    attributes = ['Order ID', 'Order_type', 'Security', 'Direction', 'Size',
                  'Status', 'Arrival_time']

    def __init__(self, direction: str, size: int, security: str):
        super().__init__(direction, size, security)
        self.order_type = 'Market'

    def __str__(self):
        return 'Order ID: \t{}\n'.format(self.order_id) + \
            'Order Type: \t{}\n'.format(self.order_type) + \
            'Security: \t{}\n'.format(self.security) + \
            'Direction: \t{}\n'.format(self.direction) + \
            'Size: \t\t{}\n'.format(self.size) + \
            'Status: \t{}\n'.format(self.status) + \
            'Arrival time: \t{}\n'.format(self.arrival_time)

    def get_order_type(self):
        return self.order_type

    def to_series(self):
        return pd.Series(data=[self.get_order_id(), self.get_order_type(),
                               self.get_security(), self.get_direction(),
                               self.get_size(), self.get_status(),
                               self.get_arrival_time()],
                         index=MarketOrder.attributes,
                         name=self.get_order_id())

class LimitOrder(Order):
    attributes = ['Order ID', 'Order_type', 'Security', 'Direction', 'Size',
                  'Price_limit', 'Status', 'Arrival_time', 'Is_iceberg_peak']

    def __init__(self, direction: str, size: int, price_limit: float, security='AMZN',
                 is_iceberg_peak=False):
        super().__init__(direction, size, security)
        self.price_limit = price_limit
        self.order_type = 'Limit'
        self.is_iceberg_peak = is_iceberg_peak

    def __str__(self):
        return 'Order ID: \t{}\n'.format(self.order_id) + \
            'Order Type: \t{}\n'.format(self.order_type) + \
            'Security: \t{}\n'.format(self.security) + \
            'Direction: \t{}\n'.format(self.direction) + \
            'Size: \t\t{}\n'.format(self.size) + \
            'Status: \t{}\n'.format(self.status) + \
            'Arrival time: \t{}\n'.format(self.arrival_time)

    def get_price_limit(self):
        return self.price_limit

    def get_order_type(self):
        return self.order_type
    
    def get_is_iceberg_peak(self):
        return self.is_iceberg_peak

    def to_series(self):
        return pd.Series(data=[self.get_order_id(), self.get_order_type(),
                               self.get_security(), self.get_direction(),
                               self.get_size(), self.get_price_limit(),
                               self.get_status(), self.get_arrival_time(),
                               self.get_is_iceberg_peak()],
                         index=LimitOrder.attributes,
                         name=self.get_order_id())


class IcebergOrder(Order):

    def __init__(self, direction: str, iceberg_order_size: int, price_limit: float, security: str, peak_size: int):
        super().__init__(direction=direction, size=iceberg_order_size, security="AMZN")
        self.order_type = "Iceberg"
        self.peak_size = peak_size
        self.peak_order = LimitOrder(direction=direction, size=peak_size,
                                     price_limit=price_limit, security=security,
                                     is_iceberg_peak=True)

    def get_peak_size(self):
        return self.peak_size

    def get_peak_order(self):
        return self.peak_order

    def update_peak_order_arrival_time(self):
        self.peak_order.arrival_time = dt.datetime.now()

    def update_peak_order_size(self, updated_size: int):
        self.peak_order.update_size(updated_size=updated_size)

    def update_iceberg_order_size(self, updated_size: int):
        self.update_size(updated_size=updated_size)




if __name__ == '__main__':
    m1 = MarketOrder(direction='Sell', size=3000, security="AMZN")
    l1 = LimitOrder(direction='Buy', size=500, price_limit=1600, security="AMZN")
    l2 = LimitOrder(direction='Buy', size=100, price_limit=1700, security="AMZN")
    l3 = LimitOrder(direction='Buy', size=3000, price_limit=1750, security="AMZN")
    ib1 = IcebergOrder(direction='Buy', iceberg_order_size= 1000, security='AMZN', peak_size=100, price_limit=1500)
