#Price Action Long Strategy
import yfinance as yf

#Simple Moving average formula 
def simpleMovingAverage(df, length, value):
    return sum(df.iloc[-length:][value]) / length

# Function to sort the list of tuples by its second item 
def Sort_Tuple(tup):  
      
    # getting length of list of tuples 
    lst = len(tup)  
    for i in range(0, lst):  
          
        for j in range(0, lst-i-1):  
            if (tup[j][1] > tup[j + 1][1]):  
                temp = tup[j]  
                tup[j]= tup[j + 1]  
                tup[j + 1]= temp  
    return tup  

#Meets buying conditions
#For this strategy, the buying condition is when the equity has high volume on a green day.
#Volume > Volume Average
#Today's Close > Yesterday's Close
#Today's Close > Yesterday's Open
#Today's Close > Today's Open
def buyConditionsMet(todaysEquityData, yesterdaysEquityData, volumeAverage_50, priceAverage, strategy):
    condition_1 = todaysEquityData['Volume'] >= yesterdaysEquityData['Volume']
    condition_2 = todaysEquityData['Volume'] >= volumeAverage_50 * .8
    condition_3 = todaysEquityData['Close'] > priceAverage

    condition_4 = todaysEquityData['Open'] >= yesterdaysEquityData['Open']
    condition_5 = todaysEquityData['Close'] > todaysEquityData['Open']

    pullback_1 = yesterdaysEquityData['Volume'] >= volumeAverage_50 
    pullback_2 = yesterdaysEquityData['Close'] > yesterdaysEquityData['Open']
    pullback_3 = todaysEquityData['Close'] < todaysEquityData['Open']
    pullback_4 = todaysEquityData['Close'] > yesterdaysEquityData['Open'] and todaysEquityData['Close'] < yesterdaysEquityData['Close']
    
    if strategy == 'breakout':
        return condition_1 and condition_2 and condition_3 and condition_4 and condition_5
    elif strategy == 'pullback':
        return pullback_1 and pullback_2 and pullback_3 and pullback_4

    return False

#Profit Target = (1 + reward) * Purchase Price
#Stop Loss = (1 - risk) * Purchase Price
def tradeResult(todaysEquityData, tomorrowsEquityData, risk, reward):
    tradePrice = todaysEquityData['Close']

    if (tomorrowsEquityData['Open'] >= tradePrice * (1 + reward)) or (tomorrowsEquityData['Low'] > tradePrice * (1 - risk) and tomorrowsEquityData['High'] >= tradePrice * (1 + reward)):
        return "Win"
    elif(tomorrowsEquityData['Low'] <= tradePrice * (1 - risk)):
        return "Lose"

    return "Stale"

#Analyze a trade for a given symbol
def analyzeTrade(ticker, risk, reward, leverage, show_full_logs, strategy):
    tickerData = yf.Ticker(ticker)
    tickerDataFrame = tickerData.history(period='1d', start = '2018-1-1', end='2020-8-18')
    days = len(tickerDataFrame)

    wins = 0                           #How many times the strategy wins
    losses = 0                         #How many times the strategy looses
    stale = 0                          #Neither a win nor a loss

    for day in range(1, days - 1): #days - 1
        todaysEquityData = tickerDataFrame.iloc[day]   #High, Low, Open, Close, of a given day
        yesterdaysEquityData = tickerDataFrame.iloc[day - 1]    #High, Low, Open, Close, of a yesterday
        tomorrowsEquityData = tickerDataFrame.iloc[day + 1]     #High, Low, Open, Close, of a tomorrow

        volumeAverage_50 = simpleMovingAverage(tickerDataFrame.iloc[0: day], 50, 'Volume')     #50 Day Volume Average
        priceAverage = simpleMovingAverage(tickerDataFrame.iloc[0: day], 50, 'Close')                                       #Can set this to a SMA value 

        todaysDate = tickerDataFrame.index[day]

        if(buyConditionsMet(todaysEquityData, yesterdaysEquityData, volumeAverage_50, priceAverage, strategy)):
            result = tradeResult(todaysEquityData, tomorrowsEquityData, risk, reward)

            if(show_full_logs):                                 #Prints the trade date and the result of the trade. Only runs on show_full_logs = True
                print(todaysDate)
                print(result)

            if(result == "Win"):
                wins += 1
            elif(result == "Lose"):
                losses += 1
            else:
                stale += 1

    win_percent = wins / (wins + losses + stale)
    loss_percent = losses / (wins + losses + stale)
    stale_percent = stale / (wins + losses + stale)

    expected_value = (win_percent * reward - loss_percent * risk) * leverage

    return [("Ticker", ticker), ("Wins", wins), ("Losses", losses), ("Stales", stale), ("Win%", win_percent), ("Loss%", loss_percent), ("Stale%", stale_percent), ("ExpVal", expected_value + 1)]

#METHODS TO BE EXECUTED BY index.py
#----------------------------------------
#----------------------------------------

#Given a ticker, do a deep analysis and return the average expected value, optimal reward point, and highest expected value 
def optimizeTicker(ticker, risk, reward_risk_ratios, leverage, show_full_logs, strategy):
    max_expected_value = 0
    optimal_profit_target = 0
    total_expected_value = 0

    for reward_risk_ratio in reward_risk_ratios: 
        print("Analyzing {} with a Stop Loss of {}% and a profit target of {}%".format(ticker, risk * 100, risk * reward_risk_ratio * 100))
        trade = analyzeTrade(ticker, risk, risk * reward_risk_ratio, leverage, show_full_logs, strategy)

        if(trade[7][1] > max_expected_value):
            max_expected_value = trade[7][1]
            optimal_profit_target = risk * reward_risk_ratio
        total_expected_value += trade[7][1]
        print("Result: ")
        print(trade)
    
    average_expected_value = total_expected_value / len(reward_risk_ratios)

    print('---------------------------')
    print(ticker)
    print('---------------------------')
    print('Average Expected Value: {}'.format(average_expected_value))
    print('Optimal Take Profit %: {}%'.format(optimal_profit_target * 100))
    print('Expected Value at {}% Take Profit: {}'.format(optimal_profit_target * 100, max_expected_value))
    print('Est. Annual Return at Optimal Take Profit: {}'.format(max_expected_value ** 260))
    print('')

    return [average_expected_value, optimal_profit_target, max_expected_value]

#Given a quote of stocks, return the optimal risk reward points and its expected value 
def optimizeTrades(tickers, risk, reward_risk_ratios, leverage, strategy):
    results = []
    for ticker in tickers: 
        results.append(optimizeTicker(ticker, risk, reward_risk_ratios, leverage, False, strategy))

    print('--------------------------')
    print('OPTIMIZED TRADES')
    print('--------------------------')

    total_expected_value = 0

    for x in range(0, len(tickers)):
        total_expected_value += results[x][2]
        print('Buy {} at a {}% take profit target. Expected Value is {}'.format(tickers[x], results[x][1] * 100, results[x][2]))
    
    print('-----')
    print('Total Expected Value: {}'.format(total_expected_value / len(tickers)))
    print('Est. Annual Expected Value: {}'.format((total_expected_value / len(tickers)) ** 260))
        
#Given a list of tickers, sort them by average expected value 
def sortTickersByExpectedValue(tickers, risk, reward_risk_ratios, leverage, strategy):
    pairs = []
    for ticker in tickers: 
        result = optimizeTicker(ticker, risk, reward_risk_ratios, leverage, False, strategy)
        pairs.append([ticker, result[2]])

    pairs = Sort_Tuple(pairs)

    index = len(pairs)
    for pair in pairs: 
        print('{}: {} has MAX expected value of {}'.format(index, pair[0], pair[1]))
        index -= 1
        print('')

    return pairs

