
from collections import deque
import order_class as oc
class IcebergManager():

    def __init__(self):
        self.fifo_buffer = deque()

    def insert_iceberg_order(self, iceberg_order):
        self.fifo_buffer.append(iceberg_order)

    def pop_iceberg_order(self):
        return self.fifo_buffer.popleft()

















