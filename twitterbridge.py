# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

# Twitter developer credentials
CONSUMER_KEY = "--REPLACE--"
CONSUMER_SECRET = "--REPLACE--"
OAUTH_TOKEN = "--REPLACE--"
OAUTH_TOKEN_SECRET = "--REPLACE--"

def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth
    

def getFollowers(screenName, cursor):
	method = "followers/list.json?screen_name="+ screenName + "&count=200&cursor=" + cursor
	return _get(method)

def getFriends(screenName, cursor):
	method = "friends/list.json?screen_name="+ screenName + "&count=200&cursor=" + cursor
	return _get(method)

def getUsers(screenNames):
    method = "users/lookup.json?screen_name=" + screenNames

    return _get(method)

def _get(req):

	oauth = get_oauth()
	url = "https://api.twitter.com/1.1/"+ req
	r = requests.get(url=url, auth=oauth);
	return r
