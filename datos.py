"""
Capa de datos
"""

#imports
import pymongo
import yfinance as yf
from GoogleNews import GoogleNews

'''
Base de datos
'''
#conexión a cliente
client = pymongo.MongoClient("mongodb://localhost:27017/")

#conexión a db
db = client["NYSE"]

#selección de colección
col = db["Users"]


def get_user(username):
    query = { "username": username }
    result = list(col.find(query))
    if result == []:
        return False
    elif len(result)>1:
        raise Exception("Nombre de usuario repetido")
    else:
        return result[0]

def add_user(username,password):
    if get_user(username):
        return False
    else:
        newuser = { "username": username, "password": password, "stocks": ["AAPL","DIS","FB","TSLA","NFLX","AMZN","GOOG"] }
        col.insert_one(newuser)
        return newuser


def update_user(stocks,user):
    myquery = { "username": user["username"] }
    newvalues = { "$set": { "stocks": stocks } }
    col.update_one(myquery, newvalues)
    return get_user(user["username"])



'''
API
'''

rating_systems = {"Sell": ["Strong Sell","Sell","Moderate Sell","Weak Hold","Underweight","Reduce","Underperform","Negative","Sector Underperform","Market Undererform","Below Average","Underperformer"],
                  "Neutral" : ["Hold","Neutral","Equal-Weight","Equal-weight","Sector Perform","Market Perform","Perform","Sector Weight","In-Line","Fair Value","Peer Perform","Average"],
                  "Buy" : ["Buy","Moderate Buy","Accumulate","Overweight","Add","Strong Buy","Long-term Buy","Long-Term Buy","Market Outperform","Positive","Outperform","Sector Outperform","Market Outperform","Overperformer"]}



def get_all_stocks_info(stocks):
    result = []
    for sym in stocks:
        result.append(get_stock_info(sym))
    return result


def get_stock_info(sym):
        result = []
        ticker = yf.Ticker(sym)
        if list(ticker.history()["Close"]) == []:
            return ["-","-","-","-","-",[]]
        result.append(str(list(ticker.history()["Close"])[-1]))
        result.append("{0:+06.2f}".format(float(result[0]) - list(ticker.history()["Close"])[-2]))
        try:
            rating = get_rating(list(ticker.recommendations["To Grade"]))
            if rating >= 50:
                result.append("Buy ("+str(rating)+")")
            elif rating <= -50:
                result.append("Sell ("+str(rating)+")")
            else:
                result.append("Hold ("+str(rating)+")")
        except:
            result.append("-")
        try:
            result.append(str(float(ticker.dividends[-1])))
        except:
            result.append("-")
        try:
            result.append(ticker.options[0])
        except:
            result.append("-")
        try:
            f = list(ticker.recommendations["Firm"])
            r = list(ticker.recommendations["To Grade"])
            for i in range(len(r)):
                if r[i] in rating_systems["Sell"]:
                    r[i] = r[i]+"0"
                elif r[i] in rating_systems["Neutral"]:
                    r[i] = r[i]+"1"
                elif r[i] in rating_systems["Buy"]:
                    r[i] = r[i]+"2"
            l = list([i+": "+j for i,j in zip(f,r)])
            result.append(l)
        except:
            result.append("-")
    
        return result


def get_rating(recs):
    score = 0
    
    for r in recs:
        if r in rating_systems["Sell"]:
            score -= 1
        elif r in rating_systems["Neutral"] or r == "":
            pass
        elif r in rating_systems["Buy"]:
            score += 1
        else:
            print("Rating not recognized -------- ", r)
    return score

def get_news():
    googlenews = GoogleNews()
    googlenews.setlang('en')
    return googlenews.search("Stock Market")
        