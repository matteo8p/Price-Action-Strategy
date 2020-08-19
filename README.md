# Price Action Trading Strategy 
### Written by Matthew Wang 8/18/2020

The Price Action Trading Strategy is an overnight play examining price and volume of a security on the daily charts. The idea is to buy the equity at price close, then sell it for a profit the next morning. This program optimizes this strategy by analyzing the win probability and expected outcome. Law of large numbers states that repeating this strategy a large number of times will result in approaching the true expected value derived from the simulation. 

# The Strategy
The strategy is to buy on a bullish candle supported by high volume. Aim to buy the stock right at market close (3:30 - 4:00 pm) so that prices do not flucuate too much after purchase. This should be done every day. Set a GTC_EXT order at profit target for morning next day. At 6:15 am next day, some equities may be sold by the GTC_EXT order. For those that have not been executed, set up an OCO bracket with profit target and Stop Loss. Let the stocks play out during market hours. Repeat again at end of day. 

The risk is ~1% 
The profit target is range from 1% - 3%

## Buy Conditions
Buy on a bullish candle supported by high volume 

    Volume > Volume Average(50)
    Today's Close > Yesterday's Close
    Today's Close > Yesterday's Open
    Today's Close > Today's Open

See PriceActionStrategy.buyConditionsMet() to see the logic

## Win Condition
Essentially, if you hit your profit target, it's a win. If the price goes below risk, it's a loss. If neither, it's a stale 

The logic is here: 

    if(tomorrowsEquityData['Open'] > tradePrice * (1 - risk)) and (tomorrowsEquityData['High'] >= tradePrice * (1 + reward)):
        return "Win"
    elif(tomorrowsEquityData['Low'] <= tradePrice * (1 - risk)):
        return "Lose"

    return "Stale"      

# Program Execution 
Main method of the program is at index.py.
Configure your variable constants: 

    ticker = 'CNX'
    watchlist = ['AMZN', 'TSLA', 'GOOG', 'W', 'BDX', 'TDOC', 'CRM', 'ENTG', 'JD', 'PTON', 'TRMB', 'STNE', 'BJ', 'NRG']
    ticker_set = ['PTON', 'FUTU', 'HCAT', 'TSLA', 'TDOC']
    risk = 0.01
    reward_risk_ratios = [1, 1.5, 2, 2.5, 3]
    leverage = 1

Decide which function you want to run 

    init(0) will run PriceActionStrategy.optimizeTicker(). This will do a analysis of the 'ticker' constant above
    init(1) will sort your watchlist based on average expected return value 
    init(2) will optimize your risk-reward of the stocks in ticker_set 

Once your variables are configured, execute python 

    python index.py

# How you should use the program 
1. Build your watchlist of stocks that appear to meet the criteria and look good
2. Run your watchlist sort 

    init(1)

3. Choose the best ~5 stocks or so. (However many you want to diversify risk)
4. Optimize the best ~5 stocks to buy for the day 

    init(2)

5. Execute the strategy mentioned above

