import sys
sys.path.append("./python")

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import reddit_keyword_counter_extension

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    keyword = data['keyword']
    subreddit_names = data['subreddit_names']
    start_date = data['start_date']
    end_date = data['end_date']

    # Call your keyword_counter function with the given parameters
    result = reddit_keyword_counter_extension.process_data(keyword, subreddit_names, start_date, end_date)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
