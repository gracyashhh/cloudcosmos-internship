import praw
import pandas as pd
import datetime
import json
import csv

#API details
reddit = praw.Reddit(client_id='-EEHQleeInOcvK3IAvyDnA',client_secret='FlXDttBu3mK6xn61pV4-FOADxeqawg',username='Web_reddit',password='webscrap123',user_agent='webscrap model')

#first tried by getting top and hot comments of big data
print("-----------------------BIG DATA----------------------------")
bd_data = reddit.subreddit('BigData').top(limit=10)
bigData = []
for d in bd_data:
    print("Author:",d.author)
    print("Title:",d.title)
    print("ID:", d.id)
    t = d.created
    r_date = datetime.date.fromtimestamp(t)
    r_time = datetime.datetime.fromtimestamp(t)
    print("Date and Time:",r_time)
    # comment_list = d.comments                 #printing comments
    # for comment in comment_list:
    #     print("Comment:",comment.body)
    bigData.append([d.author,d.id,d.title,r_date,d.url])
    print(45*'-')

bd_hot = reddit.subreddit('BigData').hot(limit=10)
for d in bd_hot:
    print("Author:",d.author)
    print("Title:",d.title)
    print("ID:", d.id)
    t = d.created
    r_date = datetime.date.fromtimestamp(t)
    r_time = datetime.datetime.fromtimestamp(t)
    print("Date and Time:",r_time)
    comment_list = d.comments
    for comment in comment_list:
        print("Comment:",comment.body)
    bigData.append([d.author,d.id,d.title,r_date,d.url])
    print(45*'-')


bigData = pd.DataFrame(bigData,columns=['Author','ID','Title','Date','URL'])
print(bigData)
bigData.to_csv("BigData.csv")

submission = reddit.submission(id='c5189o')
submission.comments.replace_more(limit=0)
c=0
for comment in submission.comments.list():
    c+=1
    print(comment.body)
print("No.of comments having id c5189o : is {}".format(c))


#scraping contents in wallstreetbets page

print("-----------------wallstreetbets----------------------------")

wall = reddit.subreddit('wallstreetbets').hot(limit=50)
wallStreet = []                             #list used to store the details
for post in wall:
    print("Author:", post.author)
    print("Title:", post.title)
    print("ID:", post.id)
    t = post.created
    r_date = datetime.date.fromtimestamp(t)
    r_time = datetime.datetime.fromtimestamp(t)
    print("Date and Time:", r_time)
    print("Upvote:",post.ups)
    # comment_list = post.comments
    # for comment in comment_list:
    #     print("Comment:", comment.body)
    wallStreet.append([post.author,post.id, post.title, r_date, post.num_comments, post.score, post.upvote_ratio, post.url])
    print(65 * '-')

#storing the details got in the list in .csv and .json format
print("-----------------Dataset----------------------------")
wallStreet = pd.DataFrame(wallStreet,columns=['Author','ID','Title','Date','No.of comments','Score','Upvote','URL'])
print(wallStreet)
wallStreet.to_csv("wallstreetbets.csv")

with open ("wallstreetbets.csv","r",encoding="utf8") as f:
    reader = csv.reader(f)
    next(reader)
    data = []
    for row in reader:
        data.append({"Author":row[1],"post_id":row[2],"Title":row[3],
                              "Date":row[4],"No.of comments":row[5],"Score":row[6],
                              "Upvote":row[7],"URL":row[8]})

with open('wallstreetbets.json','w') as f:
    json.dump(data,f,indent=4)