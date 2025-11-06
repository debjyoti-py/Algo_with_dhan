
import pdb
import time
import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib
import matplotlib.pyplot as plt

client_code = "1107610379"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzYyMzU4NjM5LCJpYXQiOjE3NjIyNzIyMzksInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTA3NjEwMzc5In0.0mnk1BlY99Q7X-UUVVO_COVBuQ0ECCAtGCdEJ86YXXoEzAPNzbQ2Ic5yx36BdgOj12CSr4rMfJ0Tiur76qHUFg"

tsl         = Tradehull(client_code,token_id)
data  = tsl.get_historical_data(tradingsymbol = 'SBIN',exchange = 'NSE' ,timeframe="5")



pdb.set_trace()
data  = tsl.get_historical_data(tradingsymbol = 'NIFTY',exchange = 'INDEX' ,timeframe="DAY")

tsl.get_historical_data("SENSEX 27 DEC 78500 CALL", exchange="BFO", timeframe="5")

ltp   = tsl.get_ltp_data(names = ['NIFTY DEC FUT'])


data.sort_values(by="close")


new_chart = data.set_index(data['timestamp'])
# or
new_chart = data.set_index(data['timestamp']);  # Add a semicolon to separate the statement

# Add a new line and move the next statement to a new line
new_chart = data.set_index(data['timestamp'])

# Average volume & institutaional volume 

average_volume = data.describe()['volume']['mean']
inst_volume    = data[data["volume"] > 3*average_volume]

