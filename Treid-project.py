# Import

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
import pandas as pd
import json
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import time
import os

def Data_Treid(name, date_begin, date_end, accuracy):
  date_begin_unix = int(time.mktime(time.strptime(date_begin, '%Y-%m-%d %H:%M:%S')))
  date_end_unix = int(time.mktime(time.strptime(date_end, '%Y-%m-%d %H:%M:%S')))

  url = 'https://api.bcs.ru/udfdatafeed/v1/history?symbol=' + name + '&resolution=' + accuracy + '&from=' + str(date_begin_unix) + '&to=' + str(date_end_unix)
  print('Request for: ',url)
  response = requests.get(url)
  print('Respose status = ', response.status_code)
  if response.status_code != 200:
    print(" Error url")
  else:
    soup = BeautifulSoup(response.text, features='html.parser')
    data_soup = soup.text
    dictData = json.loads(data_soup)
    arr = pd.DataFrame({'Date':dictData["t"], 'C':dictData['c'], 'O':dictData['o'], 'H':dictData['h'], 'L':dictData['l'], 'V':dictData['v']})
    arr.Date = arr.Date.map(lambda p: datetime.utcfromtimestamp(p).strftime('%Y-%m-%d %H:%M:%S'))
    arr = arr.set_index('Date')
    print('Receiving data from ', arr.index[0], 'to', arr.index[-1], 'with step = ', (dictData["t"][1]-dictData["t"][0]),' s')
    print('Quantity = ',len(arr.C))
    print('Successfully')
    return arr

if __name__=="main":
   Test = Data_Treid('GAZP', '2021-11-23 18:30:00', '2021-11-23 23:22:00', '1')
   ax = Test.O.plot(alpha=0.5, title="My graph", ylabel=" o - ")
   print("Количество данных = ",len(Test.O))
   ax.set_yscale('log')
   print("ОТКР = ",Test.O[-1]) 
   print("МАКС = ",Test.H[-1]) 
   print("ЗАКР = ",Test.C[-1]) 
   print("МИН = ",Test.L[-1])
   print(Test.V[-1])