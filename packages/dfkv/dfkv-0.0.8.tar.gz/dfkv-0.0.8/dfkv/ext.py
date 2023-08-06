# this is ext utils
from datetime import datetime, date

def now(type = 1) -> str:
    """1: 2023-04-06 15:38:34.267
    2: 2023-04-06 15:38:34.267
    3: 20230406153834267
    4: 20230406153834
    5: 2023-04-06
    6: 20230406
    """
    if type == 1:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    elif type == 2:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif type == 3:
        return datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    elif type == 4:
        return datetime.now().strftime("%Y%m%d%H%M%S")
    elif type == 5:
        return date.today().strftime("%Y-%m-%d")
    elif type == 6:
        return date.today().strftime("%Y%m%d")
    
    else:
        return datetime.now()

if __name__ == "__main__":
    print(now(5))
    print(now(6))
    print(now(99))