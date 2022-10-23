from flask import Flask, jsonify, request
import re

app = Flask(__name__)

def remove_emoji(line):
    return line.encode('ascii', 'ignore').decode("utf-8")

def remove_enter(line):
    return line.replace('\n','')

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

if __name__ == "__main__":
    app.run(port=1234,debug=True)