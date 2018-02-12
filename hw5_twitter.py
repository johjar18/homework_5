from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching


# on startup, try to load the cache from file
CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(twitter_cache.json, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets
baseurl= 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params= {'screen_name': username, 'count': num_tweets}
response= requests.get(baseurl, params, auth=auth)
json_data= json.loads(response.text)
# print(json.dumps(json_data, indent=4))

new_file= open('tweet.json', 'w')
new_file.write('json_data')
new_file.close()
# print(json.dumps(json_data, indent=4))




#Code for Part 2:Analyze Tweets
tweet_list= []
for tweet_data in json_data:
    tweet_text= tweet_data['text']
    # print(tweet_text)
    tweet_list.append(tweet_text)
    # print(tweet_list)



    #
    # tokens = nltk.word_tokenize(all_list)
    # print(tokens)
    # freqDist = nltk.FreqDist(token for token in tokens if token.isalpha() and "http" not in token)
    #
    # for word, frequency in freqDist.most_common(5):
    #
    #     freq= word + " " + str(frequency)
    #     print(freq)

#
# split_tweet= tweet_text.split()
freq_dict = {}
#
#
for freq_count in tweet_text.split(" "):
    if freq_count in freq_dict:
        freq_dict[freq_count] += 1
    else:
        freq_dict[freq_count] = 1

print(freq_dict)
#
for key in sorted(freq_dict.keys()):
    print ("%s: %s" % (key, freq_dict[key]))


#     # tuple_freq= word, frequency
#     # print(tuple_freq)



# sorted_freq= sorted(freq_count, reverse=True)
# print(sorted_freq)
    # list_freq= list(freq)
    # print(list_freq)

# for items in freq:
#     print(items)


print("USER:" + username)
print("TWEETS ANALYZED:" + " " + num_tweets)
print("5 MOST FREQUENT WORDS:" + " ")




if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
