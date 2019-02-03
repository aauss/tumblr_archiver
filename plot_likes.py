import json
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
from collections import OrderedDict

def load_tumblrlike_timestamps():
    with open("posts_with_meta_information.json", 'rb') as posts:
        json_posts = json.load(posts)
    timestamps = [post['timestamp'] for post in json_posts]
    return timestamps

def transform_timestamps_to_datetime_from_posts(timestamps):
    drop_hours_and_minutes = [datetime(datetime.fromtimestamp(timestamp).year,
                                    datetime.fromtimestamp(timestamp).month,
                                    datetime.fromtimestamp(timestamp).day) for timestamp in timestamps]
    return drop_hours_and_minutes


def bin_amount_of_likes_per_day(drop_hours_and_minutes):
    cnt = Counter()
    for timestamp in drop_hours_and_minutes:
        cnt[timestamp] += 1
    ordered = OrderedDict(sorted(cnt.items()))
    return ordered

def plot_activity_and_save_plot(ordered):
    plt.figure(figsize=(8,4), dpi=100)
    plt.plot(ordered.keys(), ordered.values(), ':',color='#6a5acd')
    plt.xticks(fontname="DIN Alternate", fontsize=14)
    plt.yticks(fontname="DIN Alternate", fontsize=14)
    plt.ylabel("Number Of Articles Liked",fontname="DIN Alternate", fontsize=18)
    plt.xlabel('Year', fontname="DIN Alternate", fontsize=18)
    ax = plt.gca()
    ax.set_facecolor('#99cccc')
    plt.show()


if __name__ == '__main__':
    timestamps = load_tumblrlike_timestamps()
    datetime = transform_timestamps_to_datetime_from_posts(timestamps)
    likes_per_day_dict = bin_amount_of_likes_per_day(datetime)
    plot_activity_and_save_plot(likes_per_day_dict)
