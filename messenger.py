
class Message():

    def __init__(self, order, execution_time, execution_price, execution_size):
        self.order = order
        self.execution_time = None



class Messenger():

    def __init__(self):
        self.received_messages = {}
        self.sent_messages = {}


