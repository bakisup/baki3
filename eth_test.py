import time
import pyupbit
import datetime

access = ""
secret = ""

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)

print(get_balance("KRW-ETH"))
print(get_current_price("KRW-ETH"))
print(upbit.get_balance("KRW")) 

print("autotrade start")

# 자동매매 시작
while True:
    try:
        print("ing------------------------------")
        if get_current_price("KRW-ETH") < 5100000.0:
            krw = upbit.get_balance("KRW")
            krw = krw / 4
            print("krw")
            if upbit.get_balance("KRW") > 100000:
                upbit.buy_market_order("KRW-ETH", krw*0.9995)
                print("buy")
        if get_balance("KRW-ETH") > 0:
            if get_current_price("KRW-ETH") > 5300000.0:
                ETH = get_balance("KRW-ETH")
                print("sell")
                upbit.sell_market_order("KRW-ETH", ETH*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
