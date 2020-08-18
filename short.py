#Price Action SHORT Strategy

import yfinance as yf


tickers = ['ELY', 'TSLA', 'ZM', 'JD', 'NVDA']

#Return the moving average of a set
#INPUTS: Dataframe, SMA Length, Desired Value (ex. 'Close')
def simpleMovingAverage(df, length, value):
    return sum(df.iloc[-length:][value]) / length

#Meets buying conditions
#For this strategy, the buying condition is when the equity has high volume on a green day.
#Volume > Volume Average
#Today's Close < Yesterday's Close
#Today's Close < Yesterday's Open
def buyConditionsMet(todaysEquityData, yesterdaysEquityData, volumeAverage_50, priceAverage_180):
    return (todaysEquityData['Volume'] > volumeAverage_50) and (todaysEquityData['Close'] < yesterdaysEquityData['Close']) and (todaysEquityData['Close'] < yesterdaysEquityData['Open'])

#Profit Target = (1 - reward) * Purchase Price
#Stop Loss = (1 + risk) * Purchase Price
def tradeResult(todaysEquityData, tomorrowsEquityData, risk, reward):
    tradePrice = todaysEquityData['Close']

    if(tomorrowsEquityData['Open'] < tradePrice * (1 + risk)) and (tomorrowsEquityData['Low'] <= tradePrice * (1 - reward)):
        return "Win"

    if(tomorrowsEquityData['High'] > tradePrice * (1 + risk)):
        return "Lose"

    return "Stale"

def getTradeProbabilities(ticker, risk, reward):
    tickerData = yf.Ticker(ticker)
    tickerDataFrame = tickerData.history(period='1d', start = '2015-1-1', end='2020-8-16')
    days = len(tickerDataFrame)

    wins = 0                           #How many times the strategy wins
    losses = 0                         #How many times the strategy looses
    stale = 0                          #Neither a win nor a loss

    for day in range(181, days - 1): #days - 1
        todaysEquityData = tickerDataFrame.iloc[day]   #High, Low, Open, Close, of a given day
        yesterdaysEquityData = tickerDataFrame.iloc[day - 1]    #High, Low, Open, Close, of a yesterday
        tomorrowsEquityData = tickerDataFrame.iloc[day + 1]     #High, Low, Open, Close, of a tomorrow

        volumeAverage_50 = simpleMovingAverage(tickerDataFrame.iloc[0: day], 50, 'Volume')     #50 Day Volume Average
        priceAverage_50 = simpleMovingAverage(tickerDataFrame.iloc[0: day], 180, 'Close')       #180 Day SMA

        todaysDate = tickerDataFrame.index[day]

        if(buyConditionsMet(todaysEquityData, yesterdaysEquityData, volumeAverage_50, priceAverage_50)):
            result = tradeResult(todaysEquityData, tomorrowsEquityData, risk, reward)

            # print(todaysDate)
            # print(result)

            if(result == "Win"):
                wins += 1
            elif(result == "Lose"):
                losses += 1
            else:
                stale += 1

    win_percent = wins / (wins + losses + stale)
    loss_percent = losses / (wins + losses + stale)
    stale_percent = stale / (wins + losses + stale)

    expected_value = win_percent * reward - loss_percent * risk

    return [("Ticker", ticker), ("Wins", wins), ("Losses", losses), ("Stales", stale), ("Win%", win_percent), ("Loss%", loss_percent), ("Stale%", stale_percent), ("ExpVal", expected_value + 1)]

def displayStats(risk, RewardRiskRatio, leverage, showIndividualTrades):
    trades = []
    for ticker in tickers:
        trade = getTradeProbabilities(ticker, risk, risk * RewardRiskRatio)
        trades.append(trade)
        if(showIndividualTrades):
            print(trade)

    sum = 0
    for trade in trades:
        sum += trade[7][1]

    payoutPerTrade = sum / len(trades) * leverage

    print("--------------------------")
    print("Risk%: {}".format(1 - risk))
    print("Reward% {}".format(1 + risk * RewardRiskRatio))
    print("Payout Per Trade: {}".format(payoutPerTrade))
    print("Est. Annual Payout: {}".format(payoutPerTrade ** 260))
    print("--------------------------")
    print("--------------------------")

def init():
    risk = .01
    RewardRiskRatio = [1, 1.5, 2]
    # RewardRiskRatio = [2]
    leverage = 1

    for rr in RewardRiskRatio:
        displayStats(risk, rr, leverage, True)

init()