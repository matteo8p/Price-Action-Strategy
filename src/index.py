import PriceActionStrategy as pas

ticker = 'ZM'
watchlist = ['YNDX', 'TECK', 'TDOC', 'PLUG', 'OSB', 'ORCL', 'KDP', 'JD', 'EXPI', 'CRSP', 'BLDP']
ticker_set = ['JD', 'PLUG', 'OSB', 'TECK', 'BLDP', 'INMD']

show_every_trade = True        #used in optimizeTicker(). Set to True to see every trade 

# 'breakout' or 'pullback' strategy
strategy = 'breakout'

risk = 0.01
reward_risk_ratios = [1, 1.5, 2, 2.5, 3]
# reward_risk_ratios = [2]
leverage = 1

#PriceActionStrategy.optimizeTicker() analyzes a single ticker
#PriceActionStrategy.optimizeTrades() analyzes the optimum take profit target for a set of given tickers
#PriceActionStrategy.sortTickersByExpectedValue() sorts a list of tickers by average expected value 

def init(run):
    #0. (OPTIONAL) To analyze a select ticker, use this method below 
    if run == 0: 
        pas.optimizeTicker(ticker, risk, reward_risk_ratios, leverage, show_every_trade, strategy)           
    elif run == 1: 
    #1. To sort your watchlist by average expected value, use this method 
        pas.sortTickersByExpectedValue(watchlist, risk, reward_risk_ratios, leverage, strategy)
    elif run == 2: 
    #Take the top 5 or so (how many stocks u wanna trade) and set your ticker_set to the top 5 or so
    #2. To optimize your risk-reward ratio for the stocks in ticker_set, use this method 
        pas.optimizeTrades(ticker_set, risk, reward_risk_ratios, leverage, strategy)

init(0)