import os
import re
import pickle
from tqdm import tqdm
from archive import download


def get_index_num(listdir):
    # Get the missing indices to know which file to retry

    index = []
    for i in range(len(listdir)):
        try:
            index.append(re.match(r'<(\d+)_?\d*>', listdir[i])[1])
        except (TypeError, IndexError):
            print(listdir[i])
    index = [int(i[:4]) for i in index]
    index = sorted(list(set(index)))
    failed_indices = set(list(range(max(index)))) - set(index)
    return failed_indices


if __name__ == '__main__':
    images = os.listdir('tumblr_images')
    videos = os.listdir('tumblr_videos')
    images.extend(videos)
    failed = get_index_num(images)

    posts_pickle = pickle.load(open('posts.p', 'rb'))

    for index in tqdm(failed):
        download([posts_pickle[index]], start=0, to_index=index, sleep=6, disable=True)


