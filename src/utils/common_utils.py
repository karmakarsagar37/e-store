import os

class CommonUtils:
    print(os.environ.get('LUCKY_ORDER_NUMBER'))
    lucky_n_number = int(str(os.environ.get('LUCKY_ORDER_NUMBER',2)))