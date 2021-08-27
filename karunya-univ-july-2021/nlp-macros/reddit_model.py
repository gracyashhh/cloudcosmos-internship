import praw
import pandas as pd

reddit = praw.Reddit(client_id='vUkzuujWwcgdgA',client_secret='znEVd_eU0gce63Nr2fbFDzhUQuQdOw',user_agent='WebScraping Model')

#posts about big data
print("---------BIG DATA---------------")
bd_post = reddit.subreddit('BigData').hot(limit=10)
for post in bd_post:
    print(post.title)

#top 10 trending posts
print("\n---------ALL---------------")
al_post = reddit.subreddit('all').hot(limit=10)
for post in al_post:
    print(post.title)

#posts about machine learning
posts = []
ml1_post = reddit.subreddit('MachineLearning')
for ml in ml1_post.hot(limit=10):
    posts.append([ml.title,ml.score,ml.id,ml.subreddit,ml.url,ml.num_comments,ml.selftext,ml.created])
posts = pd.DataFrame(posts,columns=['title','score','id','subreddit','URL','Num_comments','selftext','created'])
print("\n---------MACHINE LEARNING---------------")
print(posts)

print('\nMachine learning description:')
print(ml1_post.description)

print('\nComments on the website:')
submission = reddit.submission(url="https://www.reddit.com/r/MapPorn/comments/a3p0uq/an_image_of_gps_tracking_of_multiple_wolves_in/")
submission.comments.replace_more(limit=0)
for comment in submission.comments.list():
    print(comment.body)
