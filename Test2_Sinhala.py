#!/usr/bin/python
# coding=utf-8
import tweepy
import pandas as pd
import csv  # Import csv
import xlrd
import codecs
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize





consumer_key = '1ZFrXbH32jHTtAIz7sYAkttg6'
consumer_secret = 'kCMmzuesgQ9Ijznh7uL2gqJD1CJ1GFbhO77C8FPZ6oe7p1Fef4'
access_token = '1315870228534845442-XD2mqQGqMScZCLlXpqP5pf5h9cxsqB'
access_secret = 'EvoGd8WrX748qBcX7WC0xmDgEokIOtkI1GBBGS0pqFJJV'

tweetsIds = []  # the list containing the tweet ids
tweets = []  # the list containing the tweets

# opening the csv file  and getting the twitter id coloumns
csvfile = open('get_tweets.csv', encoding="utf-8")


readCSV = csv.reader(csvfile, delimiter=',')
for row in readCSV:
    if (row and row[1] != ''):
        tweetsIds.append(row[1])
        print(tweetsIds)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
# create a dataframe  to append tweets information
tweets_df = pd.DataFrame(columns=['ID', 'FULL TEXT', 'CREATED AT'])

for tweet in tweepy.Cursor(api.search,
                           q='#Political OR #Health OR #StateNews OR #CriminalNews OR #News',
                 lang="si", tweet_mode='extended').items():

     if (tweet.id_str not in tweetsIds) and ('RT @' not in           tweet.full_text) and (not tweet.retweeted):
        # create a dataframe from the existing information
        df = pd.DataFrame([[ tweet.id_str, tweet.full_text, tweet.created_at]],
                          columns=['ID', 'FULL TEXT', 'CREATED AT'])

        # append it to the tweets_df
        tweets_df =  tweets_df.append(df , ignore_index=True)


print ( tweets_df)
with open('get_tweets.csv', 'a', encoding="utf-8") as f:
    tweets_df.to_csv(f, header=f.tell() == 0)

#remove punctuation, English letters and create a new csv file 7/2/2021
excel_file_path = 'get_tweets.csv'
df = pd.read_csv(excel_file_path)
print(df.head(2))
df['FULL TEXT'] = df['FULL TEXT'].str.replace(r'[A-z,a-z,{P}!@#$%&\'()"*+,-./:;<=>?@^_`{|}~♦👇👈👉😁😂🛳🤣🙂📌🌳🤔▶🔻🤷]',"")
df.to_csv("removed_characters.csv")

# remove stopwords  2/3/2021

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

with codecs.open('StopWords.txt', 'r', encoding='utf8') as stop_word_data:
 stop_words = stop_word_data.read()
tokenized_stop_word = tokenizer.tokenize(stop_words)
stop_word_list = []
for stop_words in tokenized_stop_word:
 stop_words_sentence = stop_words.split()
 for word in stop_words_sentence:
  stop_word_list.append(word)
for word in stop_word_list:
  print(word)

excel_file_path = 'removed_characters.csv'
new_list = []
df = pd.read_csv(excel_file_path, usecols = ['FULL TEXT'])
for row in df.iterrows():
 list = row[1]
 for lrow in list:
  twords = lrow.split()
  for tword in twords:
   if tword in stop_word_list:
    twords.remove(tword)
  new_list.append(twords)
  with codecs.open("removed_stopwords.txt", "a", encoding="utf-8") as output:
   output.write(str(twords))
   output.write('\n')
   output.close()




