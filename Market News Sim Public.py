#!/usr/bin/env python
# coding: utf-8

# In[21]:


# import numpy as np
import nltk
from bs4 import BeautifulSoup
from urllib.request import urlopen
from nltk.corpus import stopwords
import datetime as dt
from datetime import timedelta
import random
import requests
import pandas
import pandas_datareader as web
import html2text
import json
import tweepy
dayofweek = int(dt.datetime.today().isoweekday())
#print(dayofweek)
if not dayofweek == 5 or dayofweek == 6:

    sr = stopwords.words('english') 


    Sources = ['https://www.reuters.com/finance/markets','https://www.marketwatch.com/economy-politics?mod=top_nav']

    not_good = ["stocks","bonds","markets","drop","rise","price","2020","2021","recession","2008","2009","Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Sept", "August", "Nov", "November", "Dec", "December", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35",'shares','U.S.','prices','EDT','The',',','',' ','<','>',".","{","}"," ","#","##","###","S&P 500","DOW","MARKETS","markets","Dow Jones","-","*","|","―","__"]

    frequencies = []


    def get_tokens(source):
        url_get = requests.get(source)
        soup = BeautifulSoup(url_get.content, 'lxml')
        converted_text = html2text.HTML2Text()
        converted_text.ignore_links = True
        text = converted_text.handle(soup.prettify())
        tokens = [t for t in text.split()]
        clean_tokens = tokens[:]
        for token in tokens:
            if token in stopwords.words('english') or token in not_good:
                clean_tokens.remove(token)
            
        freq = nltk.FreqDist(clean_tokens)
        mostcommon = freq.most_common(1)
        global highestfreq
        highestfreq = text.count(mostcommon[0][0])/len(text) * 100
        #print(highestfreq)
        #freq.plot(20, cumulative=False)     
        return mostcommon

    def choose_mostcommon():
        global mostcommon
        global highestfreq
        if get_tokens(Sources[0])>get_tokens(Sources[1]):
            mostcommon = get_tokens(Sources[0])[0][0]
        else:
            mostcommon = get_tokens(Sources[1])[0][0]

    def define_performance():
        ## Setting dates
        yesterday = dt.datetime.now() - dt.timedelta(days=4)
        today = dt.datetime.now()
        N = 3
        
        ## Randomly Choosing S&P 500 or Dow Jones Industrial Average 
        randint = random.randint(1,2)
        global index_name
        if randint == 1:
            sp_or_dow = "^GSPC"
            index_name = "S&P 500"
        else:
            sp_or_dow = "^DJI"
            index_name = "Dow Jones Industrial Average"
        port = web.DataReader(sp_or_dow, 'yahoo', yesterday, today)
        port = port.drop(["Adj Close","Volume","Low","High"], axis=1)
        
        port[(port.index.dayofweek < 5) & (abs(port.index.date - dt.datetime.strptime("2017-12-25", '%Y-%m-%d').date()) > timedelta(N))]

        global percentage_change
        percentage_change = (round(((port.iat[1,1] / port.iat[0,1]) - 1) * 100,2))
        #print(percentage_change)
        #print(port)
        
        
    def form_sentence():
        global frequencies

        if percentage_change < -10:
            verb = "plummets"
        elif percentage_change <-7:
            verb = "plunges"
        elif percentage_change <-5:
            verb = "tumbles"
        elif percentage_change <0:
            verb = "sinks"
        elif percentage_change <2:
            verb = "rises"
        elif percentage_change <3:
            verb = "jumps"
        elif percentage_change <3.5:
            verb = "pops"
        elif percentage_change <4:
            verb = "surges"
        elif percentage_change <4.5:
            verb = "gains"
        elif percentage_change >4.5:
            verb = "skyrockets"
        else:
            verb = "changes"
            
        if percentage_change > 0: 
            conno = "thanks to"
        else:
            conno = "and analysts correlate the underperformance to"
        sentence = index_name + " " + verb + " "+ str(abs(percentage_change))+ " " + "percent," + " " +conno + " " +str(mostcommon)
        def OAuth():
            try: 
                auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'],credentials['CONSUMER_SECRET'] )
                auth.set_access_token(credentials['ACCESS_TOKEN'],credentials['ACCESS_SECRET'])
                return auth
            except Exception as e:
                return 0
        Oauth = OAuth()
        api = tweepy.API(Oauth)

        api.update_status(sentence)    


    credentials = {}
    credentials['CONSUMER_KEY'] = ...
    credentials['CONSUMER_SECRET'] = ...
    credentials['ACCESS_TOKEN'] = ...
    credentials['ACCESS_SECRET'] = ...

    with open("twitter_credentials.json", "w") as file:
        json.dump(credentials, file)
        
    choose_mostcommon()
    define_performance()
    form_sentence()  
else:
    print()

# %%
