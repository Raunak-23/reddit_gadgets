import praw
import json
import time
import os
from pathlib import Path


# Step 1: Reddit API setup
reddit = praw.Reddit(
    client_id="5bxU6C_DISug5u0yb0cHZA",
    client_secret="l_2cGmBUJ6uTOsLM4Ya2tbf5P4rE-g",
    user_agent="mental_bot by u/FunTonight482"
)

def get_comment_tree(comment_list):
    tree = []
    for comment in comment_list:
        tree.append({
            "id": comment.id,
            "author": str(comment.author),
            "body": comment.body,
            "score": comment.score,
            "created_utc": comment.created_utc,
            "replies": get_comment_tree(comment.replies)  # ⬅ Recursive part
        })
    return tree

subreddit = reddit.subreddit("gadgets")

# Suppose you saved the last post's fullname (e.g., 't3_abc123') from yesterday
last_fullname = "t3_abc123"  # Replace with your actual last post's fullname

for submission in subreddit.new(limit=1000):
    # Fetch and print rate limit info immediately after the API call
    ratelimit_used = reddit._core._requestor._http.headers.get("x-ratelimit-used")
    ratelimit_remaining = reddit._core._requestor._http.headers.get("x-ratelimit-remaining")
    ratelimit_reset = reddit._core._requestor._http.headers.get("x-ratelimit-reset")
    print(f"Rate limit used: {ratelimit_used}, remaining: {ratelimit_remaining}, reset in: {ratelimit_reset} seconds")

    if submission.num_comments <= 10:
        continue  # Skip posts with 10 or fewer comments
    thread_url = f"https://www.reddit.com{submission.permalink}"
    print(f"Processing: {thread_url}")
    # Create a directory for the subreddit if it doesn't exist
    post_data = {
        "title": submission.title,
        "author": str(submission.author),
        "id": submission.id,
        "score": submission.score,
        "created_utc": submission.created_utc,
        "selftext": submission.selftext,
        "num_comments": submission.num_comments,
        "subreddit": str(submission.subreddit),
        "url": thread_url
    }

    # Comment parsing as before
    submission.comments.replace_more(limit=None)
    comments_tree = get_comment_tree(submission.comments)
    
    output_folder = "Prod_reddit_data"
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Save as JSON
    thread_data = {
        "post": post_data,
        "comments": comments_tree
    }

    file_path = os.path.join(output_folder, f"reddit_thread_{submission.id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(thread_data, f, indent=2)

    print(f"Saved thread: {submission.id} to {file_path}")
    time.sleep(2)