import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
df = pd.read_csv('backup_data_file.csv')

analyzer = SentimentIntensityAnalyzer()

def vadersentimentanalysis(tweet):
    vs = analyzer.polarity_scores(tweet)
    print(vs,"vs")
    return vs['compound']
df['Vader Sentiment'] = df['TWEET'].apply(vadersentimentanalysis)
print(df,"df")
print(df.columns)
def vader_analysis(compound):
    if compound >= 0.5:
        return 'Positive'
    elif compound <= -0.5 :
        return 'Negative'
    else:
        return 'Neutral'
df['Vader Analysis'] = df['Vader Sentiment'].apply(vader_analysis)
print(df.head())


df.to_csv("sentiment_on_tweets.csv")

