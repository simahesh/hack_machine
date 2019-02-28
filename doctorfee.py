#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import re


# In[3]:


data_train = pd.read_excel(r"C:\siddharth\MCL\hack machine\doctorfee\Final-Participant-Data-Folder-20190207T063931Z-001\Final Participant Data Folder\Final_Train.xlsx")
data_test = pd.read_excel(r"C:\siddharth\MCL\hack machine\doctorfee\Final-Participant-Data-Folder-20190207T063931Z-001\Final Participant Data Folder\Final_Test.xlsx")
data_test_fee = pd.read_excel(r"C:\siddharth\MCL\hack machine\doctorfee\Final-Participant-Data-Folder-20190207T063931Z-001\Final Participant Data Folder\Sample_submission.xlsx")
data_test = pd.concat([data_test,data_test_fee],axis=1)
data_train['Test']=[1 for temp in range(len(data_train))]
data_test ['Test']=[0 for temp in range(len(data_test))]
data=pd.concat([data_train,data_test])


# In[4]:


data['Experience']=data.Experience.map(lambda x: int(re.match("(\d+)",x)[1]))


# In[48]:


def qrank(x):
    cnt = x.count(',')
    if re.search('p\.*h\.*d',x,re.I):
        cnt+=5
    elif re.search('M\.*D',x,re.I):
        cnt+=3
    return cnt


# In[38]:


data.drop(['Rating','Miscellaneous_Info'],axis=1,inplace=True)


# In[41]:


data.info()


# In[49]:


data['Qrank']=data.Qualification.map(lambda x: qrank(x))


# In[50]:


data.Qrank.value_counts()


# In[54]:


data.drop(['Qualification'],axis=1,inplace=True)


# In[60]:


data.Place.fillna(data.Place.mode()[0],inplace=True)


# In[61]:


data['Place_new']=data.Place.map(lambda x: x.split()[-1])


# In[64]:


data.drop(['Place'],axis=1,inplace=True)


# In[66]:


data.info()


# In[76]:


data.Place_new.value_counts()


# In[77]:


def create_dummies( df, colname ):
    col_dummies = pd.get_dummies(df[colname], prefix=colname)
    col_dummies.drop(col_dummies.columns[0], axis=1, inplace=True)
    df = pd.concat([df, col_dummies], axis=1)
    df.drop( colname, axis = 1, inplace = True )
    return df


# In[78]:


for c_feature in ['Profile', 'Place_new']:
    #data[c_feature] = data[c_feature].astype('category')
    data = create_dummies(data , c_feature )


# In[80]:


data.shape
data.columns


# In[81]:


train_x=data[data.Test==1][data.columns.difference(['Fees','Test'])]
test_x=data[data.Test==0][data.columns.difference(['Fees','Test'])]
train_y=data[data.Test==1]['Fees']
test_y=data[data.Test==0]['Fees']


# In[94]:


train_f=pd.concat([train_x,train_y],axis=1)
test_f=pd.concat([test_x,test_y],axis=1)


# In[82]:


import statsmodels.api as sm 
train_x=sm.add_constant(train_x)
lm=sm.OLS(train_y,train_x).fit()


# In[84]:


test_x=sm.add_constant(test_x)


# In[85]:


output=lm.predict(test_x)


# In[87]:


output.to_csv(r"C:\siddharth\MCL\hack machine\doctorfee\Final-Participant-Data-Folder-20190207T063931Z-001\Final Participant Data Folder\output.csv")


# In[83]:


lm.summary()


# In[88]:


data.head()


# In[92]:





# In[99]:


data_train.plot(kind='scatter',x='Profile',y='Fees')


# In[90]:


data.Fees.value_counts()


# In[ ]:




