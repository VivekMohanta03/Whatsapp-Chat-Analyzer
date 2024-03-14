from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # no. of messages
    num_messages = df.shape[0]

    # no. of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # no. of media
    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # no. of links
    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), media, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'user': 'Name', 'count': 'Percentage Used'})

    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Fixed message omitted bug
    for index, message in df['message'].items():
        if message == '<Media omitted>\n':
            df.drop(index, inplace=True)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Fixed message omitted bug
    for index, message in df['message'].items():
        if message == '<Media omitted>\n':
            df.drop(index, inplace=True)

    words = []

    for message in df['message']:
        words.extend(message.split())
    pd.DataFrame(Counter(words).most_common(20))
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    if not len(emojis) == 0:
        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        emoji_df = emoji_df.rename(columns={0: 'Emojis', 1: 'Number of times used'})
        return emoji_df
    else:
        return None


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_time = df.groupby('onlydate').count()['message'].reset_index()
    return daily_time


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    activity_map = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_map
