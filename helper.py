import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter


def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == "<Media omitted>\n"].shape[0]

    extractor = URLExtract()

    links = []

    for message in df['message']:
        links.extend(extractor.find_urls(message))


    return num_messages,len(words),num_media_messages,len(links)

def busy_users(df):
    busy = df['user'].value_counts().head()
    df_user = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(columns={'user' : 'Name' , 'count' : 'Percentage'})
    return busy, df_user

def get_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open('stop_words_hinglish.txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep= " "))

    return df_wc

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_name']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    week = df['day_name'].value_counts()
    return week

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    month = df['month_name'].value_counts()
    return month

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    activity_table = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return activity_table

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open('stop_words_hinglish.txt', 'r')
    stop_words = f.read()

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    words_df = pd.DataFrame(Counter(words).most_common(20))

    return words_df








