# import library
import pandas as pd
from flask import Flask, request, jsonify, make_response
import sqlite3
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
import re

# connect to database
conn = sqlite3.connect('binar.db')

# define app
app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

# function to clean text
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
    
# remove punctuation
def remove_punct(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
 
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
        print("error")
        
# flask dans swagger
# call API post
@swag_from("swagger_config_post.yml", methods=['POST'])

@app.route("/text_twitter", methods=["POST"])
def twitter_text():
    request.method == "POST"
    input_text = str(request.get_json["text"])
    output_text = cleansing_data(input_text)
    sql_text = "insert into hate_speech_twitter (dirty_text,clean_text) values (?, ?)"
    result = (input_text, output_text)
    conn.execute(sql_text, result)
    conn.commit()
    print(input_text)
    print(output_text)
    return "sukses"

swagger_template = dict(
info = {
    'title': LazyString(lambda: 'percobaan membuat api swagger'),
    'version': LazyString(lambda: '1'),
    'description': LazyString(lambda: 'coba-coba'),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

#app run
if __name__ == "__main__":
    app.run(debug=True)