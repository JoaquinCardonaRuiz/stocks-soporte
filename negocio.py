"""
Capa de negocio
"""

import datos

def login(username, password):
    user = datos.get_user(username)
    if user:
        if username == user["username"] and password == user["password"]:
            return user
    else:
        return False


def add_user(username, password):
    return datos.add_user(username, password)
    

def update_user(stocks, user):
    parsed_stocks = parse_stocks(stocks)
    print(parsed_stocks)
    return datos.update_user(parsed_stocks,user)


def parse_stocks(s):
    stocks = []
    curr_str = ""
    for c in s:
        if c != ",":
            curr_str += c    
        else:
            stocks.append(curr_str)
            curr_str = ""
    stocks.append(curr_str)
    return stocks


def update_stock_data(stocks):
    return datos.get_all_stocks_info(stocks)

def update_one_stock_data(new_stocks,old_stocks,new_stock_info):
    parsed_stocks = parse_stocks(new_stocks)
    for i in range(len(old_stocks)):
        if old_stocks[i] != parsed_stocks[i]:
            new_stock_info[i] = datos.get_stock_info(parsed_stocks[i])
    return new_stock_info