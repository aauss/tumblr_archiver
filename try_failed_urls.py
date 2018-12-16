import os
import re
import pickle
from archive import download

try:
    posts_pickle = pickle.load(open('posts.p', 'rb'))
except FileNotFoundError:
    print('Your download meta data is missing. Consider download failed URLs by hand.')

failed_index = []
failed_urls = []
try:
    with open('failed_urls.txt') as handler:
        for line in handler:
            to_parse = handler.readline()
            try:
                index = re.search(r'\[(\d+)\]', to_parse)[1]
                failed_index.append(int(index))
            except TypeError:
                failed_urls.append(to_parse)
                continue
    os.remove('failed_urls.txt')
    with open('failed_urls.txt', 'a') as file:
        for failed_url in failed_urls:
            file.write(failed_url + '\n')

except FileNotFoundError:
    print('There are no failed URLs.')

posts = [posts_pickle[i] for i in set(failed_index)]
download(posts, index_of_failed=list(set(failed_index)))
