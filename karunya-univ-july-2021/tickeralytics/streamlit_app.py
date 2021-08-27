import pickle

import pandas
import streamlit as st
import pandas as pd
import altair as alt
import glob

from config import TWITTER_HANDLES

DATE_TIME_FIELD = "date"
TICKER_FIELD = "ticker"
DEFAULT_LIMIT_ROWS = 10

st.set_page_config(
    page_title="Tickeralytics!",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.header("""
Tickeralytics!
""")

@st.cache
def get_all_tweets(handles):
    all_tweets = {}
    for handle in handles:
        with open(f"twitter/{handle}_tweets.pickle", "rb") as dump_file:
            all_tweets[handle] = pickle.load(dump_file)
        break

    return all_tweets

all_tweets = get_all_tweets(TWITTER_HANDLES)
analysis = []
for handle, tweets in all_tweets.items():
    for tweet in tweets:
        print(tweet.tweet)
        if len(tweet.cashtags) > 0:
            print(tweet.cashtags)
            for cashtag in tweet.cashtags:
                analysis.append((tweet.datetime, cashtag.upper()))

data = pandas.DataFrame(analysis)
data.columns = [DATE_TIME_FIELD, TICKER_FIELD]
data.date = pd.to_datetime(data.date)
print(data)
print(data.date)


lookback_hours_dict = {'1 hour': 1, '4 hours': 4, '12 hours': 12,
                  '1 day': 24, '1 week': 24*7, '2 weeks': 24*15, '1 month': 24*30}

lookback_hours_select = st.select_slider(
    'Select a lookback period',
    options=list(lookback_hours_dict.keys()))

lookback_hours = lookback_hours_dict[lookback_hours_select]

col1, col2 = st.beta_columns(2)

def filter_data(data, hours, limit_rows=DEFAULT_LIMIT_ROWS):
    max_date_in_data = data[DATE_TIME_FIELD].max()
    cutoff_date = max_date_in_data - pd.Timedelta(hours=hours)
    hours_filtered = data[data[DATE_TIME_FIELD] > cutoff_date]

    filtered_value_counts = hours_filtered[TICKER_FIELD].value_counts()
    filtered_value_counts_reset = filtered_value_counts.reset_index()
    filtered_value_counts_reset.columns = ["ticker", "mentions"]
    return hours_filtered, filtered_value_counts_reset.head(limit_rows)

limit_rows = DEFAULT_LIMIT_ROWS
hours_filtered, filtered_value_counts_reset = filter_data(data, lookback_hours, limit_rows)
col1.write(f"Ticker mentions (top {limit_rows}) in the last {lookback_hours_select}")
col1.altair_chart(alt.Chart(filtered_value_counts_reset)
    .mark_bar().encode(y=alt.Y('ticker',  sort='-x'), x=alt.X('mentions')))

top_tickers = filtered_value_counts_reset.ticker.to_list()

col2.write(f"Ticker trendline (top {limit_rows}) in the last {lookback_hours_select}")
col2.altair_chart(alt.Chart(hours_filtered).transform_window(
        cuml='count()',
        groupby=['ticker'],
        sort=[{'field':'date'}],
        frame=[None, 0]
    ).mark_line(
    ).encode(
        x='date:T',
        y=alt.Y('cuml:Q'),
        color='ticker'
    ).transform_filter({'field': 'ticker', 'oneOf': top_tickers}))
