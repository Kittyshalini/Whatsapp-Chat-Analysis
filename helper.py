from wordcloud import WordCloud
import emoji
from collections import Counter
import datetime

def fetch_stats(selected, df):

    if selected == 'overall':
        return df.shape[0]
    else:
        return(df[df['user'] == selected].shape[0])
    
def fetch_words(selected, df):
    if(selected == 'overall'):
        return(int(df['messages'].str.len().sum()))
    else:
        return(int(df[df['user'] == selected]['messages'].str.len().sum()))
    
def fetch_media(selected, df):
    if selected == 'overall':
        num = df[df['messages'].str.strip() == '<Media omitted>'].shape[0]
    else:
        num = df[(df['user'] == selected) & (df['messages'].str.strip() == '<Media omitted>')].shape[0]
    return num

def fetch_links(selected, df):
    if selected == 'overall':
        num = df[df['messages'].str.contains('http', na=False)].shape[0]
    else:
        num = df[(df['user'] == selected) & (df['messages'].str.contains('http', na=False))].shape[0]
    return num

def fetch_busy(df):
    x = df['user'].value_counts().head()
    return x

def wordcloud_creater(selected,df):
    if selected == 'overall':
        wc = WordCloud(width=300,height=300,min_font_size=3,background_color='white')
        df = df[df['messages'].str.strip() != '<Media omitted>']
        df_wc = wc.generate(df['messages'].str.cat(sep=" "))
        return df_wc
    else:
        wc = WordCloud(width=300,height=300,min_font_size=3,background_color='white')
        df = df[(df['user'] == selected) & (df['messages'].str.strip() != '<Media omitted>')]
        df_wc = wc.generate(df['messages'].str.cat(sep=" "))
        return df_wc

def fetch_emoji(selected, df):
    emojis = []
    
    if selected == 'overall':
        messages = df['messages'].dropna()
    else:
        messages = df[df['user'] == selected]['messages'].dropna()

    for message in messages:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return Counter(emojis).most_common()

def first_msg(selected, df):
    if selected == 'overall':
        idx = df[['year', 'month', 'dates', 'hour', 'minute']].dropna().index[0]
    else:
        user_df = df[df['user'] == selected]
        idx = user_df[['year', 'month', 'dates', 'hour', 'minute']].dropna().index[0]

    row = df.loc[idx]
    return f"{row['dates']}-{row['month']}-{row['year']} {row['hour']}:{row['minute']:02d}"
