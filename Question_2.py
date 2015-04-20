
# coding: utf-8

# In[12]:

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import urllib2
import re
import sklearn


# In[13]:

filepath = '/Users/DanLo1108/Documents/Projects/Hornets/'


# In[14]:

url_list=[]
for i in range(1,21):
    url = "http://www.nbaminer.com/nbaminer_nbaminer/four_factors.php?operation=eexcel&partitionpage="+str(i)+"&partition2page=1"  
    url_list.append(url)


# In[15]:

#Gets contents of url web page 
request=urllib2.Request(url)
page = urllib2.urlopen(request)


# In[16]:

#Reads contents of page
content=page.read()
soup=BeautifulSoup(content,'lxml')


# In[17]:

table=soup.find_all('table')
results=table[0].find_all('td')


# In[19]:

#Initializes data dictionary
#Offensive and Defensive Four Factors
ff_dict = {'Team': [],
           'Off_Eff_FGperc': [],
           'Def_Eff_FGperc': [],
           'Off_FTRate': [],
           'Def_FTRate': [],
           'Off_TORate': [],
           'Def_TORate': [],
           'Off_ORRate': [],
           'Def_ORRate': [],
           'Wins': [],
           'Year': [],
           'Games': []}


# In[20]:

#Loops through results, appending statistics to their appropriate place
#in the dictionary
count = 0
for item in results[14:]:
    count += 1
    if np.mod(count,14) == 1:
        ff_dict['Team'].append(item.string)
    if np.mod(count,14) == 2:
        ff_dict['Off_Eff_FGperc'].append(float(item.string))
    if np.mod(count,14) == 3:
        ff_dict['Def_Eff_FGperc'].append(float(item.string))
    if np.mod(count,14) == 4:
        ff_dict['Off_FTRate'].append(float(item.string))
    if np.mod(count,14) == 5:
        ff_dict['Def_FTRate'].append(float(item.string))
    if np.mod(count,14) == 6:
        ff_dict['Off_TORate'].append(float(item.string))
    if np.mod(count,14) == 7:
        ff_dict['Def_TORate'].append(float(item.string))
    if np.mod(count,14) == 8:
        ff_dict['Off_ORRate'].append(float(item.string))
    if np.mod(count,14) == 9:
        ff_dict['Def_ORRate'].append(float(item.string))
    if np.mod(count,14) == 10:
        ff_dict['Wins'].append(float(item.string))
    if np.mod(count,14) == 12:
        ff_dict['Year'].append(item.string)
    if np.mod(count,14) == 0:
        ff_dict['Games'].append(float(item.string))


# In[21]:

#Creates dataframe
Four_Factors = pd.DataFrame()
for key in ff_dict:
    Four_Factors[key] = ff_dict[key]


# In[22]:

#Convers wins to wins/82 (for lockout years)
def get_wins_82(x):
    return x.Wins/x.Games*82

Four_Factors['wins_82'] = Four_Factors.apply(lambda x: get_wins_82(x), axis=1)


# In[23]:

#Changes order of columns
Four_Factors = Four_Factors[['Team','Year','Off_Eff_FGperc','Off_ORRate','Off_TORate',
                            'Off_FTRate','Def_Eff_FGperc','Def_ORRate','Def_TORate',
                            'Def_FTRate','wins_82']]


# In[24]:

#Saves to .csv
#Four_Factors.to_csv(filepath+'Four_Factors_data.csv',index=False)


# In[25]:

#Reads from .csv
#Four_Factors = pd.read_csv(filepath+'Four_Factors_data.csv')


# In[26]:

#Sets features and target for regression
X = Four_Factors[['Off_Eff_FGperc','Off_ORRate','Off_TORate',
                 'Off_FTRate','Def_Eff_FGperc','Def_ORRate','Def_TORate',
                 'Def_FTRate']]

y = Four_Factors['wins_82']


# In[34]:

#Creates linear regression model from sklearn and finds MAE from 
#random train/test splits
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier

maes=[]
for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
    linreg = LinearRegression()
    linreg.fit(X_train,y_train)
    pred = linreg.predict(X_test)

    maes.append(np.mean(abs(pred-y_test)))
    
print np.mean(maes)


# In[47]:

#Fits regression model to full dataset
linreg = linreg.fit(X,y)


# In[48]:

#Finds mean and standard deviation of 4 factors
ave_Off_Eff_FGperc = np.mean(X.Off_Eff_FGperc)
ave_Off_ORRate = np.mean(X.Off_ORRate)
ave_Off_TORate = np.mean(X.Off_TORate)
ave_Off_FTRate = np.mean(X.Off_FTRate)
ave_Def_Eff_FGperc = np.mean(X.Def_Eff_FGperc)
ave_Def_ORRate = np.mean(X.Def_ORRate)
ave_Def_TORate = np.mean(X.Def_TORate)
ave_Def_FTRate = np.mean(X.Def_FTRate)

std_Off_Eff_FGperc = np.std(X.Off_Eff_FGperc)
std_Off_ORRate = np.std(X.Off_ORRate)
std_Off_TORate = np.std(X.Off_TORate)
std_Off_FTRate = np.std(X.Off_FTRate)
std_Def_Eff_FGperc = np.std(X.Def_Eff_FGperc)
std_Def_ORRate = np.std(X.Def_ORRate)
std_Def_TORate = np.std(X.Def_TORate)
std_Def_FTRate = np.std(X.Def_FTRate)


#Predicts 41 wins with average stats
linreg.predict(np.array([ave_Off_Eff_FGperc,ave_Off_ORRate,ave_Off_TORate,
                         ave_Off_FTRate,ave_Def_Eff_FGperc,ave_Def_ORRate,
                         ave_Def_TORate,ave_Def_FTRate]))


# In[53]:

#R^2 value
r2 = linreg.score(X,y)
r2


# In[55]:

#Gets regression coefficient for Offensive Rebound Rate
orr_coef = linreg.coef_[1]
orr_coef


# In[57]:

#Gets expected win improvement from increasing ORR from .22 to .24
win_imp = orr_coef*(.24-.22)
win_imp


# In[ ]:



