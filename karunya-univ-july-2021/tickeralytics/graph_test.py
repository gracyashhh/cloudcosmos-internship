######### ROUGH SCRIPT ##########

### TWEEKING AROUND PANDAS, PLOTTING AND DATA CLEANING ###



# import plotly.graph_objects as go
# import matplotlib.pyplot as plt
# animals=['giraffes', 'orangutans', 'monkeys']
#
# fig = go.Figure(data=[
#     go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
#     go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
# ])
# # Change the bar mode
# fig.update_layout(barmode='group')
# fig
# # plt.show()
import pickle

import plotly.express as px
import pandas as pd

f1 = open('top_10', 'rb')
top_10_both = pickle.load(f1)
f1.close()
print(top_10_both,';;;;;;;;;;;;;;;;;;;')

df=pd.read_csv("sentiment_on_tweets.csv")
df2=pd.read_csv("filtered_value.csv")
result = pd.concat([df, df2], axis=1, join="inner")
result.to_csv("result.csv")
print(result)
fig = px.bar(df, x="ticker", y="date", color='Vader Analysis')
# fig.show()
print(df)
print('###########')
cnt= dict(df.ticker.value_counts())
print(dict(cnt))
print(type(cnt))
df["mentions"]=''
# for i in cnt:
#     print("key",i)
#     print("value",cnt[i])
#     # print(df.columns)
#     print(df.loc[df.ticker == i])
#     cat=df.index[df.ticker == i]
#     print(type(cat.values))
#     df.at[i, 'mentions']= cnt[i]
    # final_twitter=filtered_value_counts_reset.loc[filtered_value_counts_reset['ticker'].isin(top_10_both)]
for index, row in df.iterrows():
    df.at[index,'mentions']=cnt[row['ticker']]
print(df)

df1 = df.set_index('ticker')
# df1=[df1.apply(lambda x : df.loc[x.ticker]['Name']== x.Name , axis =1 ) ]

print(df)
cn=0
dropped=[]
for index, row in df.iterrows():
    if df.at[index,'ticker']=='AAPL':
        print('yes')
    if df.at[index,'ticker'] not in top_10_both:
        # print(row)
        cn+=1
        # print(index)
        # print(type(index))
        dropped.append(df.at[index,'ticker'])
        df.drop(index, inplace=True)
with open('debug.txt','w') as f:
    for i in dropped:
        f.write(i+" ")
print(df)
df.to_csv('check.csv')
print(f"{cn} rows dropped")
spl=df
fig = px.bar(spl, x='ticker', y='mentions',
             hover_data=['Vader Analysis','mentions'], color='Vader Sentiment',
             labels={'mentions':'Number of Mentions','ticker':'Top 10 Tickers from Twitter & Reddit'}, barmode='group',height=400)
fig.show()
print(top_10_both,'{{{{{{{{{{{{{{{{{{{{{{{{{{{')
