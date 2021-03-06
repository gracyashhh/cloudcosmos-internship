import praw
import pandas as pd
import datetime
import json
import csv
import reticker
import pickle
from data import blacklist, tick_list as ticker_list

#API details
reddit = praw.Reddit(client_id='-EEHQleeInOcvK3IAvyDnA',client_secret='FlXDttBu3mK6xn61pV4-FOADxeqawg',username='Web_reddit',password='webscrap123',user_agent='webscrap model')
#scraping contents in wallstreetbets page
print("-----------------wallstreetbets----------------------------")

wall = reddit.subreddit('wallstreetbets').top('month', limit=1000)
wallStreet = []                                             #list used to store the details
ticker = {}
ticker.clear()
print("Ticker:",len(ticker))
p_comments = {}
p_comments.clear()
print("Comments:",len(p_comments))
# u_date = datetime.date(2021,7,20)


for post in wall:
    t = post.created
    r_date = datetime.date.fromtimestamp(t)
    r_time = datetime.datetime.fromtimestamp(t)
    if len(post.selftext) > 0:                              #getting text after title
        x = post.selftext
        t = post.title
        y = t + x                                           #concatenating title and text to get tickers

        z = reticker.TickerExtractor().extract(y)           #getting tickers using reticker
        print(z)                                                                  #printing tickers

    else:
        t = post.title

        z = reticker.TickerExtractor().extract(t)           #this is when the post has no text after title
        print(z)

    post.comments_sort = 'new'
    comments = post.comments
    post.comments.replace_more(limit=0)
    for comment in post.comments.list():
        for i in z:
            if i in ticker_list and i not in blacklist:
                if i in ticker:
                    ticker[i] += 1
                    p_comments[i].append(comment.body)
                else:
                    ticker[i] = 1
                    p_comments[i] = [comment.body]
    if len(z)>0:
        for tic in z:
            if tic in ticker_list and tic not in blacklist:
                wallStreet.append([post.title, r_date, r_time, post.num_comments, post.score, post.upvote_ratio, tic])

#storing the details got in the list in .csv and .json format
print("-----------------Dataset----------------------------")
wallStreet = pd.DataFrame(wallStreet,columns=['Title','Date','Time','No.of comments','Score','Upvote','Tickers'])
print(wallStreet)
wallStreet.to_csv("wallstreetbets.csv")

# with open ("wallstreetbets.csv","w",encoding="utf8") as f:
#     reader = csv.reader(f)
#     data = []
#     for row in reader:
#         data.append({"Author":row[1],"post_id":row[2],"Title":row[3],
#         "Date":row[4],"No.of comments":row[5],"Score":row[6],
#         "Upvote":row[7],"URL":row[8],"Tickers":row[9]})
#
# with open('wallstreetbets.json','w') as f:
#     json.dump(data,f,indent=4)


fn = 'wall'
fn1 = 'ticks'
fn2 = 'comments_ls'

outfile = open(fn,'wb')
pickle.dump(wallStreet,outfile)
outfile.close()

of1 = open(fn1,'wb')
pickle.dump(ticker,of1)
of1.close()

of2 = open(fn2,'wb')
pickle.dump(p_comments,of2)
of2.close()