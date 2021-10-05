import praw
import yfinance as yf
import config
import os
import pandas as pd

reddit = praw.Reddit(client_id=config.client_id,  # your client id
                     client_secret=config.client_secret,  # your client secret
                     user_agent=config.user_agent,  # user agent name
                     username=config.username,  # your reddit username
                     password=config.password)  # your reddit password
subreddits = ['wallstreetbets', 'stocks', 'investing']

wordsToIgnore = ["SEC", "for", "and", "TA", "A"]

post_dict = {
    "title": [],  # title of the post
    "score": [],  # score of the post
    "id": [],  # unique id of the post
    "url": [],  # url of the post
    "comms_num": [],  # the number of comments on the post
    "created": [],  # timestamp of the post
    "body": []  # the descriptionof post
}
comments_dict = {
    "comment_id": [],  # unique comm id
    "comment_parent_id": [],  # comment parent id
    "comment_body": [],  # text in comment
    "comment_link_id": []  # link to the comment
}

# hotPost is a Submission of subreddit
for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    for hotPost in subreddit.hot(limit=2):
        post_dict["title"].append(hotPost.title)
        post_dict["score"].append(hotPost.score)
        post_dict["id"].append(hotPost.id)
        post_dict["url"].append(hotPost.url)
        post_dict["comms_num"].append(hotPost.num_comments)
        post_dict["created"].append(hotPost.created_utc)
        post_dict["body"].append(hotPost.selftext)

# pd = post_dict
df = pd.DataFrame.from_dict(post_dict)
tempDf = pd.read_csv("data.csv")
tickers = [[]] * len(df)
print(tickers)
searchdf = df.filter(['title', 'body'])

# Does not currently work properly
def searchCol(col):
    index = 0
    for post in searchdf[col]:
        tempTicks = tickers.pop(index)
        print(index)
        print(tempTicks)
        wordList = post.split()
        for word in wordList:
            word = word.translate({ord(i): None for i in '$.,-!'})
            if (len(word) > 5 or (word in wordsToIgnore) or (not word.isupper())):
                continue

            ticker = yf.Ticker(word)
            if (ticker.info['regularMarketPrice'] != None):
                tempTicks.append(word)
        tickers.insert(index, tempTicks)
        index+=1

for col in searchdf:
    searchCol(col)

print(tickers)

df['tickers'] = tickers


# print(df['tickers'])
# df.to_csv("data.csv")
