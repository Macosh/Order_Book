WORK IN PROGRESS

The aim of this project is to build a basic order book simulator. 

Classes include:
order_class.py - specifies attributes and methods of different types of orders: market order, limit order, etc.
orderbook_class.py - specifes attributes and methods of a 'price-time priority' order book given order types specified in order_class.py
matching_engine_class.py - specifies attributes and methods of a matching engine for order types specified in order_class.py
order_generator.py - aims to simulate a random flow of orders into an order book, with the goal of reflecting order dynamics throughout different market regimes
price_history_db.py - is a database of history or executed orders with all relevant order details - ultimately to be replaced by an SQL DB

More classes controlling flow of data between existing classes is going to be build.

