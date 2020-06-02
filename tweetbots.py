import tweepy
import time

# get these from your twitter developer api login page
consumer_key, consumer_secret = '___', '____'
access_token, access_token_secret = '___', '_'
#####

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.me()

# Create a tweet
# api.update_status('Hello again')

public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)


# api.update_status('Tweeepy + OAuth !')

# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.screen_name)

# print(public_tweets[0].text)

def limit_handle(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        time.sleep(300)
    except StopIteration:
        return


# Print the twitter handle of those I'm following
print("I'm following:")
for friend in limit_handle(tweepy.Cursor(api.friends).items()):
    print(friend.screen_name)

#Print the twitter handle of those following me
print("Following me:")
for follower in limit_handle(tweepy.Cursor(api.followers).items()):
    print(follower.screen_name)


#Generous bot: always follows-back
for follower in limit_handle(tweepy.Cursor(api.followers).items()):
    follower.follow()
    print(f"Auto-followed-back: {follower}")

# Pretentious bot: follow-back only followers who have more than 100 followers
for follower in limit_handle(tweepy.Cursor(api.followers).items()):
    if follower.followers_count  >= 100:
        follower.follow()
        print(f'Now following {follower.screen_name} who has {follower.followers_count} followers right now.')

#Narcisist bot: like any tweet with a name in it.
search_string = api.me().screen_name
numberOfTweets = 200
print(f"Now searching through the general search for {numberOfTweets} tweets that contain the string: {search_string}")
for tweet in limit_handle(tweepy.Cursor(api.search, search_string).items(numberOfTweets)):
    try:
        print(f"Found this tweet: {tweet.text}")
        tweet.favorite()
        print('Marked it as \'liked\'')
    except tweepy.TweepError as e:
        print(e.reason)
