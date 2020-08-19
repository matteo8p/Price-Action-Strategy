import PriceActionStrategy as pas

ticker = 'FUTU'
watchlist = ['AMZN', 'TSLA', 'GOOG', 'W', 'BDX', 'TDOC', 'CRM', 'ENTG', 'JD', 'PTON', 'TRMB', 'STNE', 'BJ', 'NRG', 'FUTU', 'HCAT']
ticker_set = ['PTON', 'FUTU', 'HCAT', 'TSLA', 'TDOC']

show_every_trade = False        #used in optimizeTicker(). Set to True to see every trade 

risk = 0.01
reward_risk_ratios = [1, 1.5, 2, 2.5, 3]
leverage = 1

#PriceActionStrategy.optimizeTicker() analyzes a single ticker
#PriceActionStrategy.optimizeTrades() analyzes the optimum take profit target for a set of given tickers
#PriceActionStrategy.sortTickersByExpectedValue() sorts a list of tickers by average expected value 

def init(run):
    #0. (OPTIONAL) To analyze a select ticker, use this method below 
    if run == 0: 
        pas.optimizeTicker(ticker, risk, reward_risk_ratios, leverage, show_every_trade)           
    elif run == 1: 
    #1. To sort your watchlist by average expected value, use this method 
        pas.sortTickersByExpectedValue(watchlist, risk, reward_risk_ratios, leverage)
    elif run == 2: 
    #Take the top 5 or so (how many stocks u wanna trade) and set your ticker_set to the top 5 or so
    #2. To optimize your risk-reward ratio for the stocks in ticker_set, use this method 
        pas.optimizeTrades(ticker_set, risk, reward_risk_ratios, leverage)

init(0)