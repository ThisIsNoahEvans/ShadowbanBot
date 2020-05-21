import urllib.request
import sys
import tweepy
import time

class colour:
    purple = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    red = '\033[91m'
    bold = '\033[1m'
    end = '\033[0m'

auth = tweepy.OAuthHandler("API", "API")
auth.set_access_token("API", "API")
api = tweepy.API(auth)
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

print(colour.blue, colour.bold, 'Imported Libraries, Connected to Twitter API, Defined User Agent')

with open ('/home/noah/Desktop/Shadowban Bot/users.txt') as usersFile:
    print('Opened users file')
    for line in usersFile:
        username = str(line)
        username = username.replace('\n', '')
        username = username.replace('@', '')
        print(colour.blue, 'Removed @ and blank line from username')
        #Get api content
        url = "https://shadowban.eu/.api/" + username
        headers={'User-Agent':user_agent,} 
        request=urllib.request.Request(url,None,headers)
        print('Getting response from Shadowban.eu API...')
        response = urllib.request.urlopen(request)
        data = response.read()
        data = str(data)
        print('Successfully read data from Shadowban.eu and saved to a string.', colour.end)

        #Check if it exists
        if '{"profile": {"exists": true,' in data:
            print(colour.purple, 'Account exists', colour.end)
        else:
            #If account does not exist, move to next account in list
            print(colour.red, colour.bold, 'Account does not exist', colour.end)
            continue

        #Check if it is suspended
        if '"suspended": true,' in data:
            #If account is suspended, move to next account in list
            print(colour.red, colour.bold, 'Account is suspended', colour.end)
            continue
        else:
            print(colour.purple, 'Account is not suspended', colour.end)

        #Check if it is private
        if '"protected": true,' in data:
            #If account is private, move to next account in list
            print(colour.red, colour.bold, 'Account is private', colour.end)
            continue
        else:
            print(colour.purple, 'Account is public', colour.end)
        
        #Check if it has Tweets
        if '"has_tweets": true' in data:
            print(colour.purple, 'Account has Tweets', colour.end)
        else:
            #If account has no Tweets, move to next account in list
            print(colour.red, colour.bold, 'Account has no Tweets', colour.end)
            continue

        #Check if it is shadowbanned (ghost ban)
        if '{"ghost": {"ban": false' in data:
            #If account is not shadowbanned, compose negative Tweet
            print(colour.purple, colour.bold, 'Account is not shadowbanned', colour.end)
            tweet = '@' + username + ', you are not shadowbanned. We\'ll check again tomorrow and let you know.'
            try:
                api.update_status(tweet)
                print(colour.green, colour.bold, 'TWEETED:', tweet)
            except:
                print(colour.red, colour.bold, 'ERROR SENDING TWEET.', colour.end)
            print(colour.blue, colour.bold, 'Waiting 5 minutes to run tests on next account...', colour.end)
            time.sleep(300)
            continue
        else:
            #If account is shadowbanned, compose positive Tweet
            print(colour.purple, colour.bold, 'Account is shadowbanned', colour.end)
            tweet = '@' + username + ', you are shadowbanned. We\'ll check again tomorrow and let you know.'
            try:
                api.update_status(tweet)
                print(colour.green, colour.bold, 'TWEETED:', tweet)
            except:
                print(colour.red, colour.bold, 'ERROR SENDING TWEET.', colour.end)
            print(colour.blue, colour.bold, 'Waiting 5 minutes to run tests on next account...', colour.end)
            time.sleep(300)
            continue