import praw
import pandas as pd
import datetime
import json
import csv

reddit = praw.Reddit(client_id='-EEHQleeInOcvK3IAvyDnA',client_secret='FlXDttBu3mK6xn61pV4-FOADxeqawg',username='Web_reddit',password='webscrap123',user_agent='webscrap model')
user = reddit.redditor('mutantdustbunny')
submissions = user.submissions.new(limit=None)
self_text = []
users = []
for link in submissions:
    self_text.append(link.selftext)
    sub = reddit.submission(id=link)
    sub.comments.replace_more(limit=10)
    print("Title:",sub.title)
    t = sub.created
    r_date = datetime.date.fromtimestamp(t)
    users.append([sub.author,sub.id, sub.title, r_date, sub.num_comments, sub.score, sub.upvote_ratio, sub.url])
    for comment in sub.comments.list():
        if len(comment.body)>0:
            print("Comments:")
            print(comment.body)
    print(50*'-')

users = pd.DataFrame(users,columns=['Author','ID','Title','Date','No.of comments','Score','Upvote','URL'])
print(users)
users.to_csv('user_data.csv')

with open ("user_data.csv","r",encoding="utf8") as f:
    reader = csv.reader(f)
    next(reader)
    data = []
    for row in reader:
        data.append({"Author":row[1],"post_id":row[2],"Title":row[3],
                              "Date":row[4],"No.of comments":row[5],"Score":row[6],
                              "Upvote":row[7],"URL":row[8]})

with open('user_data.json','w') as f:
    json.dump(data,f,indent=4)