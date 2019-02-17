import json
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
from collections import OrderedDict

###############################
##Amount of likes plot#########
###############################


def plot_amount_of_likes():
    timestamps = load_tumblrlike_timestamps()
    datetimes = transform_timestamps_to_datetime_from_posts(timestamps)
    likes_per_day_dict = bin_amount_of_likes_per_day(datetimes)
    plot_activity_and_save_plot(likes_per_day_dict.keys(), likes_per_day_dict.values(), 'Number Of Articles Liked')


def transform_timestamps_to_datetime_from_posts(timestamps_of_likes):
    drop_hours_and_minutes = [datetime(datetime.fromtimestamp(timestamp).year,
                                       datetime.fromtimestamp(timestamp).month,
                                       datetime.fromtimestamp(timestamp).day) for timestamp in timestamps_of_likes]
    return drop_hours_and_minutes


def bin_amount_of_likes_per_day(drop_hours_and_minutes):
    cnt = Counter()
    for timestamp in drop_hours_and_minutes:
        cnt[timestamp] += 1
    ordered = OrderedDict(sorted(cnt.items()))
    return ordered


###############################
##Time spent on Tumblr plot####
###############################

def plot_time_spent():
    timestamps = load_tumblrlike_timestamps()
    days_timestamp_dict = create_date_timestamp_dict(timestamps)
    day_time_spent_dict = calc_day_time_spent_dict(days_timestamp_dict)
    day, time = sort_day_time_spent_values(day_time_spent_dict)
    plot_activity_and_save_plot(day, time, 'Minutes Spent On Tumblr')


def calc_day_time_spent_dict(days_timestamp_dict):
    days_timestamp_dict_copy = deepcopy(days_timestamp_dict)
    for key in days_timestamp_dict_copy.keys():
        list_of_timestamps = days_timestamp_dict_copy[key]
        if len(list_of_timestamps) > 1:
            seconds_spent_this_day = get_total_difference_in_seconds(pairwise_times(days_timestamp_dict_copy[key]))
        else:
            seconds_spent_this_day = 150
        days_timestamp_dict_copy[key] = seconds_spent_this_day
    return days_timestamp_dict_copy

def sort_day_time_spent_values(days_timestamp_dict):
    sorted_by_value = sorted(days_timestamp_dict.items(), key=lambda key_value: key_value[0])
    x = [i[0] for i in sorted_by_value]
    y = [i[1]/60 for i in sorted_by_value]
    return x, y


def pairwise_times(datetime_iterable):
    # t -> (t0,t1), (t1,t2), (t2, t3), ..."
    later, earlier = tee(datetime_iterable)
    next(earlier, None)
    return zip(later, earlier)


def get_total_difference_in_seconds(datetime_tuple_iterable):
    deltas_seconds = [(later - earlier)
                      for later, earlier in sorted(datetime_tuple_iterable, reverse=True)]
    # If the time between two likes is larger than five minutes, it is probably another Tumblr session.
    deltas_seconds_adjusted = [min(delta.seconds, 300) for delta in deltas_seconds]
    return sum(deltas_seconds_adjusted)


def create_date_timestamp_dict(timestamps):
    dates = [datetime.fromtimestamp(timestamp)
             for timestamp in timestamps]

    days_timestamp_dict = defaultdict(list)
    for date in dates:
        days_timestamp_dict[
            datetime(date.year, date.month, date.day)
        ].append(date)
    return days_timestamp_dict


def plot_activity_and_save_plot(x, y, x_label):
    plt.figure(figsize=(8, 4), dpi=100)
    plt.plot(x, y, ':', color='#6a5acd')
    plt.xticks(fontname="DIN Alternate", fontsize=14)
    plt.yticks(fontname="DIN Alternate", fontsize=14)
    plt.ylabel(x_label, fontname="DIN Alternate", fontsize=18)
    plt.xlabel('Year', fontname="DIN Alternate", fontsize=18)
    ax = plt.gca()
    ax.set_facecolor('#99cccc')
    plt.savefig(f'{x_label}.png')
    plt.show()


def load_tumblrlike_timestamps():
    with open("posts_with_meta_information.json", 'rb') as posts:
        json_posts = json.load(posts)
    timestamps_of_likes = [post['timestamp'] for post in json_posts]
    return timestamps_of_likes


if __name__ == '__main__':
    plot_amount_of_likes()
    plot_time_spent()
