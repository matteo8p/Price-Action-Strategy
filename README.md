# Price Action Trading Strategy 
### Written by Matthew Wang 8/18/2020

The Price Action Trading Strategy is an overnight play examining price and volume of a security on the daily charts. The idea is to buy the equity at price close, then sell it for a profit the next morning. This program optimizes this strategy by analyzing the win probability and expected outcome. Law of large numbers states that repeating this strategy a large number of times will result in approaching the true expected value derived from the simulation. 

# The Strategy
The strategy is to buy on a bullish candle supported by high volume. 

1. Select the top stocks to buy that day 
2. Divide your portfolio and buy the stocks at end of day (3:30 - 4:00 pm). Try to hit the 'close' price as close as possible
3. After market closes, create GTC_EXT limit order for profit targets. 
4. Wake up at 6:00 - 6:15 am. Some of your stocks may be executed by the GTC_EXT order 
5. For the stocks that have not executed, create an OCO bracket with Stop Loss and Profit Target Limit Order 
6. Let your OCO orders play out for the day. 
7. Repeat strategy near market close. 

Throughout the steps, use the program to optimize your stock choices and risk reward ratios. 

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

    if(tomorrowsEquityData['Low'] > tradePrice * (1 - risk)) and (tomorrowsEquityData['High'] >= tradePrice * (1 + reward)):
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

    python -m pip install yfinance (If needed)
    python src/index.py

# How you should use the program 
1. Build your watchlist of stocks that appear to meet the criteria and look good
2. Run your watchlist sort 

    init(1)

3. Choose the best ~5 stocks or so. (However many you want to diversify risk)
4. Optimize the best ~5 stocks to buy for the day 

    init(2)

5. Execute the strategy mentioned above

