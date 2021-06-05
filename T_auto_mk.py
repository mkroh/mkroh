import time
import pyupbit
import datetime

access = "bShtj8vZlxmrgDMDeSfdM42fczQon0z0L9eJxd05"
secret = "wWVFk4FHnhr8ba3KN6JsqHGOUofOdxbj466SQmU4"

# 대상 ticker 입력
ticker = "KRW-XRP"



def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=1)
    start_time = df.index[0]
    return start_time

def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=15)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma5_1(ticker):
    """1봉전 5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=15)
    ma5_1 = df['close'].rolling(5).mean().iloc[-2]
    return ma5_1

def get_ma20_1(ticker):
    """1봉전 20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=30)
    ma20_1 = df['close'].rolling(20).mean().iloc[-2]
    return ma20_1

def get_ma60_1(ticker):
    """1봉전 60일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=70)
    ma60_1 = df['close'].rolling(60).mean().iloc[-2]
    return ma60_1

def get_ma120_1(ticker):
    """1봉전 120일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=130)
    ma120_1 = df['close'].rolling(120).mean().iloc[-2]
    return ma120_1

def get_ma240_1(ticker):
    """1봉전 240일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=250)
    ma240_1 = df['close'].rolling(240).mean().iloc[-2]
    return ma240_1                

def get_vol_1(ticker):
    """1봉전 거래량 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=5)
    vol_1 = df['volume'].iloc[-2]
    return vol_1

def get_vol_2(ticker):
    """2봉전 거래량 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=5)
    vol_2 = df['volume'].iloc[-3]
    return vol_2

def get_open_1(ticker):
    """1봉전 시가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=5)
    open_1 = df['open'].iloc[-2]
    return open_1

def get_low_1(ticker):
    """1봉전 저가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=5)
    low_1 = df['low'].iloc[-2]
    return low_1

def get_close_1(ticker):
    """1봉전 종가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=5)
    close_1 = df['close'].iloc[-2]
    return close_1



def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]



# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


now = datetime.datetime.now()
start_time = get_start_time(ticker)
end_time = start_time + datetime.timedelta(minutes=3)

ma5 = get_ma5(ticker)
ma5_1 = get_ma5_1(ticker)
ma20_1 = get_ma20_1(ticker)
ma60_1 = get_ma60_1(ticker)
ma120_1 = get_ma120_1(ticker)
ma240_1 = get_ma240_1(ticker)
vol_1 = get_vol_1(ticker)
vol_2 = get_vol_2(ticker)
open_1 = get_open_1(ticker)
low_1 = get_low_1(ticker)
close_1 = get_close_1(ticker)
current_price = get_current_price(ticker)
avg_buy_price = upbit.get_avg_buy_price(ticker)
balances = upbit.get_balances()
balance = upbit.get_balance(ticker)


# 자동매매 시작
while True:
    try:
        
        if avg_buy_price > current_price*1.01:
            upbit.sell_market_order(ticker, balance)

        elif avg_buy_price < current_price*0.98:
            upbit.sell_market_order(ticker, balance)

        elif start_time < now < end_time - datetime.timedelta(seconds=10):
        
            if ma240_1 < ma120_1 < ma60_1 and ma20_1 < ma5_1 and vol_2*2 < vol_1 and open_1 < close_1 and open_1 < ma5_1 < close_1 and ma5 < current_price:
                krw = upbit.get_balance("KRW")
                if krw > 10000:
                    upbit.buy_market_order(ticker, 10000/current_price)






        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)