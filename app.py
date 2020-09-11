# Import the necessary packages

import numpy as np
from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt

app = Flask(__name__)


# function to calculate the percentage of different polarities

def percentage(part, whole):
    return 100 * float(part) / float(whole)


# Create the route for the web app for rendering the front end i.e. index.html file
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    final_features = [np.array(int_features)]

    '''
        Obtain your Credentials from Your Twitter's developer account and assign to them to the variables
    '''
    consumerKey = "**************"
    consumerSecret = "********************"
    accessToken = "**************************"
    accessTokenSecret = "********************************"

    '''
        Obtain authorization access to twitter's api by writing the folowing code
    '''
    auth = tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    '''
        Obtain the tweets by following the below syntax
    '''
    tweets = tweepy.Cursor(api.search, q=final_features[0][0], language="English").items(int(final_features[0][1]))
    noOfSearchTerms = int(final_features[0][1])
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    '''
        Iterate through tweets and analyze the polarities
    '''
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity

        if (analysis.sentiment.polarity == 0):
            neutral += 1
        elif (analysis.sentiment.polarity < 0):
            negative += 1
        elif (analysis.sentiment.polarity > 0):
            positive += 1
    positive = percentage(positive, noOfSearchTerms)
    negative = percentage(negative, noOfSearchTerms)
    neutral = percentage(neutral, noOfSearchTerms)
    polarity = percentage(polarity, noOfSearchTerms)

    positive = format(positive, '0.2f')
    negative = format(negative, '0.2f')
    neutral = format(neutral, '0.2f')

    '''
        Check the polarity of the Topic
    '''
    if (polarity == 0.00):
        output = "Neutral"
    elif (polarity < 0.00):
        output = "Negative"
    elif (polarity > 0.00):
        output = "Positive"
    '''
        Now Return the output to the Front end
    '''
    return render_template('index.html', prediction_text='Overall Sentiment : {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)