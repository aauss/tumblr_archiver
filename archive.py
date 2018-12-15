#!/usr/bin/python
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


def new_oauth(yaml_path):
    '''
    Return the consumer and oauth tokens with three-legged OAuth process and
    save in a yaml file in the user's home directory.
    '''

    print('Retrieve consumer key and consumer secret from http://www.tumblr.com/oauth/apps')
    consumer_key = input('Paste the consumer key here: ')
    consumer_secret = input('Paste the consumer secret here: ')

    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    # STEP 1: Obtain request token
    oauth_session = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth_session.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    # STEP 2: Authorize URL + Rresponse
    full_authorize_url = oauth_session.authorization_url(authorize_url)

    # Redirect to authentication page
    print('\nPlease go here and authorize:\n{}'.format(full_authorize_url))
    redirect_response = input('Allow then paste the full redirect URL here:\n')

    # Retrieve oauth verifier
    oauth_response = oauth_session.parse_authorization_response(redirect_response)

    verifier = oauth_response.get('oauth_verifier')

    # STEP 3: Request final access token
    oauth_session = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier
    )
    oauth_tokens = oauth_session.fetch_access_token(access_token_url)

    tokens = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': oauth_tokens.get('oauth_token'),
        'oauth_token_secret': oauth_tokens.get('oauth_token_secret')
    }

    yaml_file = open(yaml_path, 'w+')
    yaml.dump(tokens, yaml_file, indent=2)
    yaml_file.close()

    return tokens


def get_token():
    # Get token
    yaml_path = os.path.expanduser('~') + '/.tumblr'
    yaml_file = open(yaml_path, "r")
    tokens = yaml.safe_load(yaml_file)
    yaml_file.close()
    # Use token to be able to use the client
    client = pytumblr.TumblrRestClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret'])
    assert client.likes()["liked_count"] > 1

    return client


def save(url, content_type, index, tags):
    # A saver function for downloading content based on URL

    try:
        os.mkdir('tumblr_videos')
    except FileExistsError:
        pass
    try:
        os.mkdir('tumblr_images')
    except FileExistsError:
        pass
    tags = tags[:150]  # Otherwise name gets to long
    if content_type == "video":
        try:
            path = os.path.join('videos', str(index) + tags + '.mp4')
            urllib.request.urlretrieve(url, path)
        except:
            with open("failed_urls.txt", "a") as file:
                file.write(url + ' Index:[' + index + ']' + "\n")
    else:
        try:
            img_data = requests.get(url).content
            path = os.path.join('images', str(index) + tags + '.jpg')
            with open(path, 'wb') as handler:
                handler.write(img_data)
        except:
            with open("failed_urls.txt","a") as file:
                file.write(url + ' Index:[' + index + ']' + "\n")


def find_first_post(client):
    now = int(time.time())
    past = time.mktime(datetime.strptime("01/02/2007", "%d/%m/%Y").timetuple())
    timestamp = now - (now - past)/2
    posts = client.likes(before=now, limit=51)['liked_posts']
    while len(posts) in [0, 51]:
        posts = client.likes(before=int(timestamp), limit=51)['liked_posts']
        if len(posts) == 0:
            past = timestamp
            timestamp = now - (now - past)/2
        elif len(posts) == 51:
            now = timestamp
            timestamp = now - (now - past)/2
    print('Starting with your first post at {}'.format(datetime.utcfromtimestamp(timestamp).strftime('%Y %m %d %H:%M')))
    posts = client.likes(before=int(timestamp), limit=51)['liked_posts']
    try:
        first_post_timestamp = min([posts[k]['liked_timestamp'] for k in range(len(posts))])
    except ValueError:
        print('Your account seems to be too fresh or you have not enough posts. This script does not work :( Sorry!')
        sys.exit()
    pickle.dump(first_post_timestamp, open("first_timestamp.p", 'wb'))
    return first_post_timestamp


def api_calls_for_content(client, first_post):
    # TODO: If posts are already retrieved, only retrieve from last known one on
    checkpoint = {"caused_error_url": [],
                  "not_found_contenttype": [],
                  "offsets": [first_post],
                  "name_dict": {},
                  "num_post": 0,
                  "current_api_call": 0}
    posts = []
    try:
        likes = client.likes()["liked_count"]
        iterations = int(likes / 51 + 1)
        for _ in tqdm(range(iterations)):
            # Iterate over batches of size 49 to create as little requests as possible
            request = client.likes(after=checkpoint["offsets"][-1], limit=51)
            new_offset = max([request["liked_posts"][k]['liked_timestamp'] for k in range(len(request["liked_posts"]))])
            checkpoint["offsets"].append(new_offset)
            posts.extend(request["liked_posts"])
    except ValueError: 
        with open('posts_with_meta_information.json', 'w') as json_file:
            json.dump(posts, json_file)
        pickle.dump(posts, open("posts.p", 'wb'))
    return posts


def download(posts, start=0):
    # Download likes
    index = 0
    try:
        for index, post in enumerate(tqdm(posts[start:])):
            time.sleep(3)
            index += start
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
                    except KeyError:
                        pass
                else:
                    pass
    finally:
        pickle.dump(index, open('checkpoint.p', 'wb'))


if __name__ == '__main__':
    yaml_path = os.path.expanduser('~') + '/.tumblr'
    try:
        client = get_token()
    except (AssertionError, FileNotFoundError):
        new_oauth(yaml_path)
    client = get_token()
    print("Getting an overview...\n")
    if os.path.isfile('first_timestamp.p'):
        first_post = pickle.load(open('first_timestamp.p', 'rb'))
    else:
        first_post = find_first_post(client)
    print('Gently asking Tumblr to tell what you liked.')
    if os.path.isfile('posts.p'):
        posts = pickle.load(open('posts.p', 'rb'))
    else:
        posts = api_calls_for_content(client, first_post)
    print("Start downloading. Each file gets a number and its tags as a name.")
    print("A file (failed_urls.txt) might be written with stuff that did not work. "
          "Download it yourself later. Don't be surprised to find many videos blocked though.")
    if os.path.isfile('checkpoint.p'):
        start = pickle.load(open('checkpoint.p', 'rb'))
        download(posts, int(start))
    else:
        download(posts)
    # TODO: Add a function to then try failed URLs again
