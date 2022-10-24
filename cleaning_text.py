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
    text = re.sub('xf0 x9f x98 x84 xf0 x9f x98 x84 xf0 x9f x98 x84',' ',text)
    return text

# remove punctuation
def remove_punct(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    return text

# cleansing data    
def cleansing_data(text):
    text = lowercase(text) 
    text = remove_emoji(text)
    text = remove_bytes_character(text)
    text = remove_unneeded_char(text)
    text = remove_punct(text)
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
    conn = sqlite3.connect('binar.db')
    first_column = input_file.iloc[:, 0]
    print(first_column)

    for hate_speech_twitter in first_column:
        clean_text = cleansing_text(hate_speech_twitter)
        sql_tabel = "insert into hate_speech_twitter (dirty_text,clean_text) values (?, ?)"
        res = (hate_speech_twitter, clean_text)
        conn.execute(sql_tabel, res)
        conn.commit()
        print(hate_speech_twitter)