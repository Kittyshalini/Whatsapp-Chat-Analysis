import re
import pandas as pd

def preprocess(data):
    
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message':message, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    df.rename(columns={'message_date':'date'}, inplace=True)
    df = df.iloc[1:,:]

    user = []
    messages = []

    def separate_name(sentence):
      index = sentence.find(':')
      user.append(sentence[0:index])
      messages.append(sentence[index+1:])
      return

    df['user_message'] = df['user_message'].apply(separate_name)

    df['user'] = pd.DataFrame(user)
    df['messages'] = pd.DataFrame(messages)

    df.drop(columns = ['user_message'], inplace = True)

    df.reset_index(inplace = True, drop = True)

    year = []
    month = []
    dates = []
    hour = []
    minute = []

    def get_data(sentence):
      year.append(sentence.year)
      month.append(sentence.month_name())
      dates.append(sentence.day)
      hour.append(sentence.hour)
      minute.append(sentence.minute)

    df['date'] = df['date'].apply(get_data)

    df['year'] = pd.DataFrame(year)
    df['month'] = pd.DataFrame(month)
    df['dates'] = pd.DataFrame(dates)
    df['hour'] = pd.DataFrame(hour)
    df['minute'] = pd.DataFrame(minute)

    df.drop(columns = ['date'], inplace = True)

    return(df)