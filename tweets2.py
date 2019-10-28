import tweepy
import csv #Import csv
import unidecode
import time

CONSUMER_KEY = 'KpRjwTE2FkHQUyN6sB4Rh98r6'
CONSUMER_SECRET = 'Vcjnq9u4icEXsmUjm6nWDUMUSgFnBikCHiZZJJ5c9YA9CCoLsa'

ACCESS_TOKEN = '341265145-whsC9REq52dSN6HuY5pte0Hn1kSvfmn72zWtMqIu'
ACCESS_SECRET = 'SzJ5JYRURyz5xOOlNgH1dY1HJgoZgyqHof06fC4UgWLkd'
i=0
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, retry_count=100, retry_delay=5, wait_on_rate_limit=True, wait_on_rate_limit_notify=False)

    # Iterate through all tweets containing the given word, api search mode
    # Lista de atributos de un tweet:
    # created_at, id, id_str, text, source, truncated, in_reply_to_status_id, in_reply_to_status_id_str,
    # in_reply_to_user_id, in_reply_to_user_id_str, in_reply_to_screen_name, quoted_status_id, 
    # quoted_status_id_str, is_quote_status, quoted_status, retweeted_status, quote_count,
    # reply_count, retweet_count, favorite_count, favorited, retweeted, possibly_sensitive,
    # filter_level, lang, matching_rules, current_user_retweet, scopes, withheld_copyright,
    # withheld_in_countries, withheld_scope
    # User:
    # id, id_str, name, screen_name, location, derived, url, description, protected, verified,
    # followers_count, friends_count, listed_count, statuses_count, created_at, profile_banner_url,
    # profile_image_url_https, default_profile, default_profile_image, withheld_in_countries,
    # withheld_scope
    # More info at: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
with open("results2.csv", 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['id', 'Created at','texto','hashtags','source','reply count', 'retweet count', 'favorite count', 'lang', 'user id', 'user id string', 
    'user screen name', 'user location', 'user verified', 'user followers count', 'user friends count', 'created at'])
    text = ""
    reply_count=""
    for tweet in tweepy.Cursor(api.search, "FullSaborParaEnamorarMas", lang="es", tweet_mode="extended").items():
        i=i+1
        try:
            text = unidecode.unidecode(tweet.retweeted_status.full_text)
        except AttributeError:
            text = unidecode.unidecode(tweet.full_text)
        created=tweet.created_at
        source=tweet.source
        if hasattr(tweet, 'reply_count'):
            reply_count = tweet.reply_count
        else:
            reply_count = ""
        retweet_count = tweet.retweet_count
        favorite_count = tweet.favorite_count
        lang = tweet.lang
        hashtags = []
        for hashtag in tweet.entities.get('hashtags'):
            hashtags.append(unidecode.unidecode(hashtag['text']))
        userid = tweet.user.id 
        userid_str=tweet.user.id_str
        user = unidecode.unidecode(tweet.user.name)
        location = unidecode.unidecode(tweet.user.location)
        verified = tweet.user.verified
        followers_count = tweet.user.followers_count
        friends_count = tweet.user.friends_count
        listed_count = tweet.user.listed_count
        created_at =tweet.user.created_at
        writer.writerow([i, created, text,str(hashtags),source,reply_count, retweet_count, favorite_count, lang, userid, userid_str, user, 
        location, verified, followers_count, friends_count, created_at])
        #writer.writerow([favorite_count])
        time.sleep(0.25)
        print("Trabajando",i)