from flask import Flask, jsonify, request
import re
import pandas as pd

app = Flask(__name__)

def remove_emoji_csv(line):
    return re.sub(r"\\x[A-Za-z0-9./]+", "", line)

def remove_emoji(line):
    return line.encode('ascii', 'ignore').decode("utf-8")

def remove_enter(line):
    line = line.replace('\n',' ')
    line = line.replace('\\n',' ')
    return line

def remove_punct(line):
    return re.sub(r'[^\w\s\d]','',line)

@app.route("/post_tweet/v1", methods=['POST'])
def post_tweet():
    tweet = request.get_json()
    try:
        tweet = tweet['text']
        clean_tweet = remove_emoji(tweet)
        clean_tweet = remove_enter(clean_tweet)
        clean_tweet = remove_punct(clean_tweet)
    except Exception as e:
        print(e)
        return jsonify({"error":"kamu tidak memasukkan key text"})
    return jsonify({"clean_tweet":clean_tweet})

@app.route("/post_csv/v1", methods=['POST'])
def post_csv():
    f = request.files['file']
    df = pd.read_csv(f, encoding="latin")
    df['new_tweet'] = df.Tweet.apply(remove_emoji_csv)
    df['new_tweet'] = df.Tweet.apply(remove_enter)
    df['new_tweet'] = df.Tweet.apply(remove_punct)
    return jsonify({"clean_tweet":"success"})

if __name__ == "__main__":
    app.run(port=1234,debug=True)