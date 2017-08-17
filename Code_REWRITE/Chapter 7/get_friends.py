import twitter
consumer_key = "8ysAg8NTMr5a7wlFsFvAqjed7"
consumer_secret = "JGObWgjCf05KbhDTqhw71SHrusv7ReCK7ivtBMDGDGxIiHyGF2"
access_token = "3870126974-p3O4Kxga0vCbfx4zrTfsnTh1rfmRhoJafIRtYVX"
access_token_secret = "X3qCaciZNgFRNQdmIPSymYyLTfMev07DoDjZnCPvIdPXw"
authorization = twitter.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
t = twitter.Twitter(auth=authorization, retry=True)

import time
import sys
import os

def get_friends(t, user_id):
    friends = []
    cursor = -1  # Start with the first page
    while cursor != 0:  # If zero, that is the end:
        try:
            results = t.friends.ids(user_id=user_id, cursor=cursor, count=5000)
            friends.extend([friends for friends in results['ids']])
            cursor = results['next_cursor']
            if len(friends) >= 10000:
                break
            if cursor != 0:
                print("Collected {} friends so far, but there are more".format(len(friends)))
                sys.stdout.flush
        except TypeError as e:
            if results is None:
                print("You probably reached your API limit, waiting for 5 minutes")
                sys.stdout.flush()
                time.sleep(5*60) # 5 minute wait
            else:
                raise e
        except twitter.TwitterHTTPError as e:
            break
        finally:
            time.sleep(60)  # Wait 1 minute before continuing
    return friends

original_users = []
tweets = []
user_ids = {}
input_filename = os.path.join("./python_tweets.json")
print(input_filename)

import json
tweets = []
with open(input_filename) as inf:
    for line in inf:
        if len(line.strip()) == 0:
            continue
        tweets.append(json.loads(line))
tweets_text = []
for tweet in tweets:
    if 'text' in tweet:
        original_users.append(tweet['user']['screen_name'])
        user_ids[tweet['user']['screen_name']] = tweet['user']['id']
        tweets_text.append(tweet['text'])

model_filename = os.path.join("./python_context.pkl")
print(model_filename)

from sklearn.externals import joblib
context_classifier = joblib.load(model_filename)
y_pred = context_classifier.predict(tweets_text)
relevant_tweets = [tweets_text[i] for i in range(len(tweets)) if y_pred[i] == 1]
relevant_users = [original_users[i] for i in range(len(tweets)) if y_pred[i] == 1]

output_filename = os.path.join("./output_python_tweets.json")
with open(output_filename, 'a') as output_file:
    test_friends = get_friends(t, user_ids[relevant_users[0]])
    for tweet in test_friends:
        if 'text' in tweet:
            #print(tweet['user']['screen_name'])
            #print(tweet['text'])
            #print()
            output_file.write(json.dumps(tweet))
            output_file.write("\n\n")
