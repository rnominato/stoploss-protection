__author__ = 'Renan Nominato'
__version__ = '0.0.1'


""""
The main purpose of this script it is verify strategies to set a optimal stoploss level. 
In this way, we tested several values of STD
"""

#TODO include pivot and other type of stoploss estimation

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import math
sns.set_style('dark')



# Generate STD and mean of a dataseries
def get_std_mean(dtf, window:int):
# Create a window specified by the user
		dft_std = dtf['Close'].rolling(window).std()
		dft_mean = dtf['Close'].ewm(span=window).mean()
		#dft_mean = dtf['Close'].rolling(window).mean()
		return [dft_std.fillna(value=dft_std.mean()), dft_mean.fillna(value=dft_mean.mean())]



#df = pd.read_pickle('XRB-BTC_T.pkl')
df = pd.read_csv('BTCUSDT08_04_sec.csv')
#df.to_csv("ex-pkl.csv")
max = len(df)
CR_dic = {"CR_max": -10000, "CR_market":-10000, "Step":1, "change_std": 0}

sing_mult= str(input('Do you want to verify a specific window? If not, we will let you know the optimal size (Y or N)'))
exc_rate  = float(input('Please define exchange fee:'))

if (sing_mult == 'Y'):
	step = int(input('Please define the # of data:'))
	max = step + 1
else:
	max = len(df)
	step = 1

for change_std in [change_std * 0.1 for change_std in range(5, 40)]:
	step = 1
	for step in range(step, math.floor(max/8)):

		df_std, df_mean = get_std_mean(df,step)
		df['MN'] = df_mean
		df['STU'] = df_mean + df_std * change_std
		df['STD'] = df_mean - df_std * change_std
		df['Dif']= (df['Close']-df['STD']) > 0
		#df['COMP'] = df['Sig'] == df['Dif']
		df['Comp'] =  df['Dif'] > 0
		df_index = 1
		CR_p = 0
		CR_result = 0
		num_opr=0

		while(df_index <= (len(df)-1)):
				if (df.iloc[df_index ]['Comp'] != df.iloc[df_index - 1]['Comp']):
						num_opr += 1

				if ((df.iloc[df_index - 1]['Comp'] == 1) & (df.iloc[df_index]['Comp'] == 0)) or \
						((df.iloc[df_index - 1]['Comp'] == 1) & (df.iloc[df_index]['Comp'] == 1)):
						CR_p = (df.iloc[df_index]['Close']/ df.iloc[df_index-1]['Close']) - 1
						CR_result += CR_p

				df_index += 1


		CR_result = ((CR_result - (num_opr*exc_rate))* 100)
		if CR_result > CR_dic["CR_max"]:
			CR_dic["CR_max"] = CR_result
			CR_dic["CR_market"] = (df.iloc[len(df)-1]['Close']/df.iloc[0]['Close']-1)*100
			CR_dic["Step"] = step
			CR_dic["change_std"] = change_std
			CR_dic["num_opr"] = num_opr




print(CR_dic)
print(CR_dic["CR_max"]-CR_dic["CR_market"])
df_std, df_mean = get_std_mean(df,CR_dic["Step"])
df['MN'] = df_mean
df['STU'] = df_mean + df_std * CR_dic["change_std"]
df['STD'] = df_mean - df_std * CR_dic["change_std"]
df.to_csv('BTCUSDT_i_b.csv')

#fig, ax = plt.subplots(2, 1, sharex=True)
#ax[0].plot (df.index, df['Close'], label='close')
#ax[0].plot (df.index, df['MN'], label='Média')
#ax[0].plot (df.index, df['STU'], label='Média+STD')
#ax[0].plot (df.index, df['STD'], label='Média-STD')
#ax[1].plot (df.index, df['Sig'], 'k')
plt.plot(df['Close'])
plt.plot(df['MN'])
plt.plot(df['STU'])
plt.plot(df['STD'])
plt.show ()
#plot with seaborn



