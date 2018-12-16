import os
import re
import pickle
from archive import *
import pytumblr
import yaml
import os
import requests
import urllib.request
import re
import pickle 
import time
import json
import sys
from datetime import datetime
from requests_oauthlib import OAuth1Session
from tqdm import tqdm
images = os.listdir()
index = []
for i in range(len(images)):
    try:
        index.append(re.match(r'(\d+)', images[i])[1])
        
    except (TypeError, IndexError):
        print(images[i])
index = [int(i[:4]) for i in index]
index = sorted(list(set(index)))
failed = set(list(range(max(index)))) - set(index)
posts_pickle = pickle.load(open('posts.p', 'rb'))
posts = [posts_pickle[i] for i in set(failed)]
for i, post in enumerate(tqdm(posts[44:])):
    time.sleep(3)
    index = list(failed)[i+44]
    if len(post) >= 1:
        content_type = post['type']
        tags = "_".join(post['tags'])
        index = str(index)
        if content_type == "photo":
            # If only one photo, download, otherwise iterate over them and download
            if len(post["photos"]) == 1:
                url = post["photos"][0]["original_size"]['url']
                save(url, content_type, index, tags)
            else:
                index += "_{}"
                for j in range(len(post["photos"])):
                    url = post["photos"][j]["original_size"]['url']
                    save(url, content_type, index.format(j), tags)
        elif content_type == "text":
            # Get the body as an HTML style string. Use Regex to extract photo URLs
            # If only one photo, download, otherwise iterate over them an download
            content = post["body"]
            url_s = re.findall(r'src="(http[s]:[\S]*media\.tumblr\.com[\S]*)"', content)
            if len(url_s) == 1:
                save(url_s[0], content_type, index, tags)
            else:
                index += "_{}"
                for j in range(len(url_s)):
                    save(url_s[j], content_type, index.format(j), tags)
        elif content_type == "video":
            # Download the video file
            try:
                url_s = post["video_url"]
                save(url_s, content_type, index, tags)
            except Exception as e:
                pass
        else:
            pass


