import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

from datetime import datetime as dt

from tvDatafeed import TvDatafeed, Interval

import seaborn as sns

################## ดึงข้อมูลจากตลาดหลักทรัพย์ ################
import requests
from PIL import Image
from io import BytesIO

def getFundFlow():
  url = getURL(symbol='',typeurl='investor_type')
  headers = {'Accept': 'application/json'}
  r = requests.get(url, headers=headers)
  data = r.json()

  d = data['oneday']['asOfDate'][0:10]
  w,m,c = [],[],[]
  for i in data['oneday']['investors']:
    nv = round(i['netValue']/1_000_000,2)
    m.append(abs(nv))
    color = 'red' if(nv<0) else 'green'
    c.append(color)
    w.append(i['type'])

  return w,m,c,d 


def getPlotFundFlow():
  w,v,color,d = getFundFlow()
  ax = plt.barh(w,v,color=color)
  plt.title('Fund Flow as of ' +d)
  c = 0
  for i in ax.patches:
    p = '-' if(color[c]=='red') else ''
    plt.text(100, i.get_y()+0.3,
             p+str(round((i.get_width()), 2)),
             fontsize=10, fontweight='bold',
             color='black')
    c+=1

    
def getURL(symbol,typeurl):
    if(typeurl=='trading-stat'):
       return  'https://www.set.or.th/api/set/stock/'+symbol+'/company-highlight/trading-stat?lang=th'
    elif(typeurl=='financial'):
       return 'https://www.set.or.th/api/set/stock/'+symbol+'/company-highlight/financial-data?lang=th'
    elif(typeurl=='sector'):
       return 'https://www.settrade.com/api/set/stock/list'
    elif(typeurl=='investor_type'):
       return 'https://www.set.or.th/api/set/market/set/investor-type-summary'

def getRatio(symbol,ratio):
  # url จากตลาดหลักทรัพย์
  try:
    url = getURL(symbol,'trading-stat')
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data[-1][ratio]
  except:
    url = getURL(symbol,'financial')
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data[-1][ratio]    
    

def getRatio_info():
  # url จากตลาดหลักทรัพย์

  rp = []
  symbol = 'ADVANC'
  url = getURL(symbol,'trading-stat')
  headers = {'Accept': 'application/json'}
  r = requests.get(url, headers=headers)
  data = r.json()  
  for i in data[-1]:
    rp.append(i)
    
  url = getURL(symbol,'financial')
  headers = {'Accept': 'application/json'}
  r = requests.get(url, headers=headers)
  data = r.json()  
  for i in data[-1]:
    rp.append(i)
  
  return list(set(rp))

def getSector():
  url = getURL(symbol='',typeurl='sector')
  resp = requests.get(url=url)
  data = resp.json()
  data = pd.DataFrame.from_dict(data['securitySymbols'])
  df = data.groupby('querySector').mean()
  for i in df.index:
    if(i!=''):
      print(i,end=' ')

def getMemberOfSector(sector):
    url = getURL(symbol='',typeurl='sector')
    resp = requests.get(url=url)
    data = resp.json()
    data = pd.DataFrame.from_dict(data['securitySymbols'])
    df = data[(data['querySector']==sector) & (~data['symbol'].str.contains('-F'))]
    return df

def getSecurities():
    url = getURL(symbol='',typeurl='sector')
    resp = requests.get(url=url)
    data = resp.json()
    data = pd.DataFrame.from_dict(data['securitySymbols'])
    return data

def getIndustry():
  url = getURL(symbol='',typeurl='sector')
  resp = requests.get(url=url)
  data = resp.json()
  data = pd.DataFrame.from_dict(data['securitySymbols'])
  data = data[['industry','querySector']] 
  data = data[data['querySector']!='']
  data = data.groupby(['industry','querySector']).mean()
  return data

def barChartWithLogo(symbol,values,title,figsize=(12,8)):
  plt.rcParams["figure.figsize"] = figsize 
  height = 2
  plt.subplots(facecolor='white')
  plt.bar(x=symbol, height=values, align='center')

  for i, (label, value) in enumerate(zip(symbol, values)):
   try:
      #print(label)  
      url = 'https://media.set.or.th/common/logo/company/'+label+'.png'
      #print(url)
      response = requests.get(url)
      #img = plt.imread(BytesIO(response.content))
      response = requests.get(url)
      img = Image.open(BytesIO(response.content))
      print(i,value,height)
      plt.imshow(img, extent=[(i - height / 5), (i + height / 5),value+(value*0.1), value+3], 
                 aspect='auto', zorder=2)
   except:
      pass
    

  plt.title(title)
  plt.xlim(-1, len(symbol) + 1)
  plt.ylim(2, max(values) *2)
  plt.tight_layout()

  plt.show()
################## End ดึงข้อมูลจากตลาดหลักทรัพย์ ################


def monthlyReturn(symbol,month,engine,market='set',plot=True):
    df = engine.tv.get_hist(symbol=symbol,exchange=market,interval=Interval.in_monthly,n_bars=month)
    
    ######
    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    
    df.Date = pd.to_datetime(df.Date)
    df['month'] = df.Date.dt.month.values
    df['year'] = df.Date.dt.year.values
    
    df['pct_change_'] = df.close.pct_change()
    df['pct_change_m'] = df['pct_change_'].shift(-1)
    
    df.drop(index=df.index[-1], 
        axis=0, 
        inplace=True)
    
    df = df.dropna()
    
    
    df['month_win'] = np.where(df.pct_change_m>=0,1,0)
    
    if(plot):
      df.groupby(df.month)['month_win'].sum().plot(kind='bar',title='monthly win')
      plt.show()
      df.groupby(df.index.month)['pct_change_m'].sum().plot(kind='bar',title='total monthly return')
        
  
      sns.set()  
      df = df.set_index('Date') 
      fig, ax = plt.subplots(figsize=(10,10))
      
      #rdgn = sns.diverging_palette(h_neg=130, h_pos=10, s=99, l=55, sep=3, as_cmap=True)
      season = df.pivot("month", "year", "pct_change_m")
      ax = sns.heatmap(season,center=0.00,cmap="PiYG",ax=ax)
      plt.title("Heatmap "+symbol+" Return")
      plt.show()  

    return df

def isset(nameVar):
    return nameVar in globals()

def rankWithRange(data,minScope,maxScope):
    basket = data.sort_values([data.columns[0]],ascending=False)

    basket['RANK'] = list(range(len(basket), 0,-1))
    maxRank = basket['RANK'].max()
    minRank = basket['RANK'].min()
    maxScope = maxScope
    minScope = minScope
    S = (minScope-maxScope)/(minRank-maxRank)
    Int = minScope - S*minRank
    basket['RS_Rank'] = basket['RANK']*S+Int  
    
    return basket

class HistStockPrice():
  def __init__(self):    
     self.tv = TvDatafeed()
    
  def days_between(self,d1, d2):
      d1 = dt.strptime(d1, "%Y-%m-%d")
      d2 = dt.strptime(d2, "%Y-%m-%d")
      return abs((d2 - d1).days)

  def getPrice(self,symbol,start,stop='',exchange='set'):
    
      date_now = dt.today().strftime("%Y-%m-%d") 
    
      if(stop==''):
        stop = date_now
    
      k = self.days_between(start, date_now)
    
      df = self.tv.get_hist(symbol=symbol,exchange=exchange,interval=Interval.in_daily,n_bars=k)
    
      df['Date'] = pd.to_datetime(df.index)
      df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
      df['Date'] = pd.to_datetime(df['Date'])

      df = df[['Date','close']]
      df = df.set_index('Date')
      df.columns = [symbol]
    
      df = df[(df.index>=start) & (df.index<=stop)]
      return df