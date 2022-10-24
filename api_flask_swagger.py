# import library
import sqlite3
import pandas as pd
from flask import Flask, request, jsonify, make_response
from cleaning_text import cleansing_data, cleansing_text, cleansing_file
from flask_swagger_ui import get_swaggerui_blueprint

# Deklarasi Flask
app = Flask(__name__)

# Connect to Database
conn = sqlite3.connect('binar.db')

# swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "hate_speech_twitter"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# home
@app.route('/', methods=['GET'])
def get():
    print ('test')
    return "hate speech twitter"

# hate_speech_twitter
@app.route("/hate_speech_twitter", methods=["GET","POST"])
def hate_speech_twitter():
    conn = sqlite3.connect('binar.db')
    if request.method == "POST":
        input_text = str(request.form["text"])
        output_text = cleansing_data(input_text)
        sql_text = "insert into hate_speech_twitter (dirty_text,clean_text) values (?, ?)"
        res = (input_text, output_text)
        conn.execute(sql_text, res)
        conn.commit()
        print(input_text)
        print(output_text)
        return output_text


    elif request.method == "GET": 
        conn = sqlite3.connect('binar.db')
        sql_text = "select * from hate_speech_twitter"
        table = conn.execute(sql_text)
        hate_speech_twitter = [
            dict(id=row[0], dirty_text=row[1], clean_text=cleansing_text(row[1]))
            for row in table.fetchall()
        ]
        return jsonify(hate_speech_twitter)

# file
@app.route("/hate_speech_twitter/csv", methods=["POST"])
def hate_speech_twitter_csv():
    if request.method == 'POST':
        file = request.files['file']
        
        
        try:
            data = pd.read_csv(file, encoding='iso-8859-1')
        except:
            data = pd.read_csv(file, encoding='utf-8') 
        cleansing_file(data)
        return cleansing_file(data)


# handling error
@app.errorhandler(404)
def error_404(error):
    return make_response(jsonify({'error': 'not found'}), 404)

@app.errorhandler(500)
def error_500(error):
    return make_response(jsonify({'error': 'server error'}), 500)

# run server
if __name__ == '__main__':    
    app.run(port = 1234, debug=True)
