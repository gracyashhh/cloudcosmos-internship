import pickle
import nltk
import squarify
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import csv
import json

#extracting from pickle file
fn = 'wall'
fn1 = 'ticks'
fn2 = 'comments_ls'

infile = open(fn,'rb')
wallStreet = pickle.load(infile)
infile.close()

inf1 = open(fn1,'rb')
ticker = pickle.load(inf1)
inf1.close()

inf2 = open(fn2,'rb')
p_comments = pickle.load(inf2)
inf2.close()

print(ticker)
#sorting ticker dict
symbols = dict(sorted(ticker.items(), key=lambda item: item[1], reverse=True))
print(symbols)
top_picks = list(symbols.keys())[0:10]
print(top_picks)
times, top = [], []
print("Top 10 tickers used:")
for i in top_picks:
    print(f"{i}: {symbols[i]}")
    times.append(symbols[i])
    top.append(f"{i}: {symbols[i]}")
print(times)
#sentimental analysis
sentiment = list(symbols.keys())
SIA = SentimentIntensityAnalyzer()
score_dict, s = {}, {}
score_dict.clear()
s.clear()
for i in sentiment:
    stock_com = p_comments[i]
    for com in stock_com:
        score = SIA.polarity_scores(com)
        if i in score:
            s[i][com] = score
        else:
            s[i] = {com:score}
        if i in score_dict:
            for key,_ in score.items():
                score_dict[i][key] += score[key]
        else:
            score_dict[i] = score
    #average calculation
    for key in score:
        a = score_dict[i][key]
        b = symbols[i]
        score_dict[i][key] = a/b
        score_dict[i][key] = "{pol:.3f}".format(pol=score_dict[i][key])

print(score_dict)
#printing sentimental analysis
print("Sentimental analysis on 10 picks:")
df = pd.DataFrame(score_dict)
df = df.T
print(df.head(10))


#converting to .csv and .json file
df.to_csv("ticker_list.csv")

with open ("ticker_list.csv","r",encoding="utf8") as f:
    reader = csv.reader(f)
    next(reader)
    data = []
    for row in reader:
        data.append({"Ticker":row[0],"Negative":row[1],"Neutral":row[2],
                                     "Positive":row[3],"Compound":row[4]})

with open('ticker_list.json','w') as f:
    json.dump(data,f,indent=4)

#data visualization
squarify.plot(sizes=times, label=top, alpha=.7)
plt.axis('off')
plt.title("Sentimental analysis on 10 picks")
plt.savefig('plot1.jpg',bbox_inches='tight',dpi=150)
plt.show()

df = df.astype(float)[:10]
colors = ['red', 'blue', 'forestgreen', 'coral']
df.plot(kind='bar', color=colors, title=f"Sentiment analysis of top 10 picks:")
plt.savefig('plot2.jpg',bbox_inches='tight',dpi=150)
plt.show()