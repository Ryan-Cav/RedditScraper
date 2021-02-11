import praw
import config
import os
import pandas as pd

reddit = praw.Reddit(client_id=config.client_id,  # your client id
                     client_secret=config.client_secret,  # your client secret
                     user_agent=config.user_agent,  # user agent name
                     username=config.username,  # your reddit username
                     password=config.password)  # your reddit password
sub = 'wallstreetbets'
subreddit = reddit.subreddit(sub)

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
for hotPosts in subreddit.hot(limit=10):
    post_dict["title"].append(hotPosts.title)
    post_dict["score"].append(hotPosts.score)
    post_dict["id"].append(hotPosts.id)
    post_dict["url"].append(hotPosts.url)
    post_dict["comms_num"].append(hotPosts.num_comments)
    post_dict["created"].append(hotPosts.created_utc)
    #post_dict["body"].append(hotPosts.body)
pd = post_dict
print(pd)
