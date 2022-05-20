import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# hello from 

saba = pd.read_csv('S_Saipa.csv')

# convert 20220518 to 2022/05/18 in pandas datetime format
saba['<DTYYYYMMDD>'] = pd.to_datetime(saba['<DTYYYYMMDD>'], format='%Y%m%d')

saba = saba.sort_values(by='<DTYYYYMMDD>')

saba = saba.set_index(pd.DatetimeIndex(saba['<DTYYYYMMDD>'].values))
# theme for plt 
plt.style.use('seaborn-whitegrid')
plt.figure(figsize=(10,5))
plt.plot(saba.index,saba['<CLOSE>'], label='KHODROO',alpha=0.3)
plt.title('KHODROO')
plt.xlabel('Date')
plt.ylabel('Price')


# moving avrage
MA30=pd.DataFrame()
MA100=pd.DataFrame()

MA30 = saba['<CLOSE>'].rolling(window=30).mean()
MA100= saba['<CLOSE>'].rolling(window=100).mean()

# plot
plt.plot(MA30, label='30 days',alpha=0.3)
plt.plot(MA100, label='100 days',alpha=0.3)

# moving avrage signal by and sell
data=pd.DataFrame()
data['price']= saba['<CLOSE>']
data['MA30']=MA30
data['MA100']=MA100



def signal(data):
    buy_sigal=[]
    sell_signal= []
    sf=-1
    
    for i in range(len(data)):
        if data['MA30'][i]>data['MA100'][i]:
            if sf!=1:
                buy_sigal.append(data['MA30'][i])
                sell_signal.append(np.nan)
                sf=1
            else:
                buy_sigal.append(np.nan)
                sell_signal.append(np.nan)
        elif data['MA30'][i]<data['MA100'][i]:
            if sf!=0:
                sell_signal.append(data['MA30'][i])
                buy_sigal.append(np.nan)
                sf=0
            else:
                buy_sigal.append(np.nan)
                sell_signal.append(np.nan)
        else:
             buy_sigal.append(np.nan)
             sell_signal.append(np.nan)
    return buy_sigal, sell_signal

data['buy_signal'] = signal(data)[0]
data['sell_signal'] = signal(data)[1]

plt.scatter(data.index,data['buy_signal'], color='g', marker='^', label='buy')
plt.scatter(data.index,data['sell_signal'], color='r', marker='v', label='sell')
            
    
    






plt.legend()
plt.show()