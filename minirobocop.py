import pdb
import pdb
import time
import talib
import datetime
import traceback
import pandas as pd
import xlwings as xw
from pprint import pprint
from Dhan_Tradehull import Tradehull

client_code = "1107610379"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzYyNzk2NTcyLCJpYXQiOjE3NjI3MTAxNzIsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTA3NjEwMzc5In0.G8hbSQyQ9Jhnf3RpJMAKZjO63x9-YCaHCF8SkU7TmiAoUhQ1Trcz326a5PgPgrps1feVwKy06HuzXkZwecKC5A"
tsl         = Tradehull(client_code,token_id)

wb            = xw.Book('Mini_robocop.xlsx')
Live_Trading  = wb.sheets['Live_Trading']
Orderbook     = wb.sheets['Orderbook']


Live_Trading.range('B2:C50').value = None
Live_Trading.range('H2:K50').value = None


bot_token           = "8549724310:AAHOJhoxbl2NPzHblsi04cRVabjREadq-UU"
receiver_chat_id    = "6193962152"

# 1. Read watchlist from excel

while True:
    watchlist    = Live_Trading.range('A2').expand('down').value
    current_time = datetime.datetime.now()
    print("While Loop Strated ", current_time, "\n\n")
    
    ltp_for_all_scripts = tsl.get_ltp_data(names = watchlist)

    for name in watchlist:
        
        
        ltp          = ltp_for_all_scripts[name]    # 2. Get Ltp data
        chart        = tsl.get_historical_data(tradingsymbol = name,exchange = 'NSE',timeframe="5") # 3. Get get_historical_data
        
        chart['rsi'] = talib.RSI(chart['close'], timeperiod=14)  # 4. Get Rsi value
        cc           = chart.iloc[-2]
        rsi_value    = round(cc['rsi'],2)
        
        
        row_no       = str(watchlist.index(name) + 2)
        Live_Trading.range('B' + row_no).value = ltp  # 5. send ltp data to excel
        Live_Trading.range('C' + row_no).value = rsi_value # 	6. send rsi value to excel
        
        
        is_this_script_traded = Live_Trading.range('J' + row_no).value
        
        buy_cell_value = Live_Trading.range('D' + row_no).value # 7. read Buy_entry_condition
        bc1            = buy_cell_value == "buy"
        bc2            = is_this_script_traded is None
        
        if bc1 and bc2:
        
            
            quantity         = Live_Trading.range('G' + row_no).value
            sl_trigger_price  = Live_Trading.range('F' + row_no).value
            
            
            
            entry_orderid  = tsl.order_placement(tradingsymbol=name ,exchange='NSE', quantity=quantity, price=0, trigger_price=0,    order_type='MARKET',     transaction_type='BUY',   trade_type='MIS')
            sl_orderid     = tsl.order_placement(tradingsymbol=name ,exchange='NSE', quantity=quantity, price=0, trigger_price=sl_trigger_price, order_type='STOPMARKET', transaction_type ='SELL', trade_type='MIS')
            
            Live_Trading.range('H' + row_no).value = entry_orderid
            Live_Trading.range('I' + row_no).value = sl_orderid
            Live_Trading.range('J' + row_no).value = "Yes_I_have_traded_this_scrip"
            Live_Trading.range('K' + row_no).value = sl_trigger_price
            
            
            message = f"name \t{name} \nrsi_value \t{rsi_value}\nquantity \t{quantity} \nsl_trigger_price \t{sl_trigger_price} \nentry_orderid \t{entry_orderid} \nsl_orderid \t{sl_orderid}"
            tsl.send_telegram_alert(message=message,receiver_chat_id=receiver_chat_id,bot_token=bot_token)
            
            pdb.set_trace()
        
    # print(row_no, name, ltp)
    
    
    
   