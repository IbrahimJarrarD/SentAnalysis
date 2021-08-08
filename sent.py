import requests
import sqlite3
import time
import re
from langdetect import detect
from translate import Translator

url = "https://google-text-analysis.p.rapidapi.com/AnalyzingSentiment"

def analysis(message):
    message = message.replace('"',"'")
    message = re.sub(r'\s+', ' ', message)
    message = re.sub(r'ツ+', '', message)
    message = re.sub(r'\\', '', message)
    try:
        lang = detect(message)
        #print(lang)
        if lang != 'en' and lang != 'de':
            translator = Translator(from_lang=lang, to_lang='en')
            message = translator.translate(message)
    except:
        pass

    payload = '{\"message\": \"'+message+'\"}'
    #print(payload)
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "d37eb7b8ccmsh95fa0d2865a1c88p1e6960jsn640096db61d2",
        'x-rapidapi-host': "google-text-analysis.p.rapidapi.com"
        }
    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)


    #print(response.text)
    score = response.json()['documentSentiment']['score']
    text_score = ''
    if -1<= score <-0.33:
        text_score = 'negative'
    elif -0.33<=score <=0.33:
        text_score = 'neutral'
    elif 0.33< score <=1:
        text_score = 'positive'
    time.sleep(1.5)
    return text_score, score


conn = sqlite3.connect('/Users/nasty/Desktop/save_pandas.db')
cur = conn.cursor()
#cur.execute('ALTER TABLE  DATA ADD COLUMN SCORE REAL NULL ')
conn.commit()

while True:
    time.sleep(2)
    conn = sqlite3.connect('/Users/nasty/Desktop/save_pandas.db')
    cur = conn.cursor()
    cur.execute('select SID,message,sentiment, score from DATA ')
    all_messages = cur.fetchall()
    cur.execute("select count(*) from DATA  where sentiment == '' or sentiment == 'nan' or score is NULL ")
    print(cur.fetchone())
#    or score is None
    for n, message,sentiment, score in all_messages:
        if sentiment == ''  or sentiment == 'nan' or score is None:
            print(type(sentiment), len(sentiment), sentiment, score)
            try:
                a_m, scores = analysis(message)
            except:
                time.sleep(1)
                a_m, scores = analysis(message)
            time.sleep(1.5)
            print(a_m,scores)
            cur.execute('update Data set Sentiment = ? where sid = ? ', [a_m, n])
            cur.execute('update Data set SCORE = ? where sid = ? ', [scores, n])
            conn.commit()
            break
    cur.close()
    conn.close()