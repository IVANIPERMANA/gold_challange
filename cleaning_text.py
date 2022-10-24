# import library
import string
import pandas as pd
import re
import sqlite3

# connect to database
conn = sqlite3.connect('binar.db')

# function to cleaning
# lowercase
def lowercase(text):
    return text.lower()

# remove emoji
def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# remove bytes character
def remove_bytes_character(text):
    return re.sub(r'[^\x00-\x7F]',' ', text)

# remove enter and unneeded chars
def remove_unneeded_char(text):
    text = re.sub('\n',' ', text)       #remove enter
    text = re.sub('user',' ', text)     #remove kata user
    text = re.sub('rt',' ', text)       #remove kata rt
    text = re.sub(r'\s+', ' ',text)     #eliminate duplicate whitespaces
    return text

# remove punctuation
def remove_punct(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    return text

# cleansing data    
def cleansing_data(text):
    text = lowercase(text) 
    print('success lowercase', text)
    text = remove_emoji(text)
    print('success remove_emoji', text)
    text = remove_bytes_character(text)
    print('success remove bytes char',text)
    text = remove_unneeded_char(text)
    print('success remove unneeded char', text)
    text = remove_punct(text)
    print('success remove punct', text)
    return text

# cleansing data for text
def cleansing_text(input_text):
    try: 
        output_text = cleansing_data(input_text)
        return output_text
    except:
        return input_text
        
# cleansing data for file
def cleansing_file(input_file):
    first_column = input_file.iloc[:, 1]
    print(first_column)
    conn = sqlite3.connect('binar.db')
    for hate_speech_twitter in first_column:
        clean_text = cleansing_data(hate_speech_twitter)
        sql_text = "insert into hate_speech_twitter (dirty_text,clean_text) values (?, ?)"
        res = (hate_speech_twitter, clean_text)
        conn.execute(sql_text, res)
        conn.commit()
        print(hate_speech_twitter)