# imports
import requests as req
import json
import urllib
from access_token import *  # Import Access token

# general variables
BASE_URL = "https://api.instagram.com/v1/"
# access token is a confidential thing, So I import it from a file I won't upload on GitHub till last submission day

DATA = []

# API calls
self_url = (BASE_URL + "users/self/?access_token=%s") % ACCESS_TOKEN
recent_self_media_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % ACCESS_TOKEN
liked_self_url = (BASE_URL + "users/self/media/liked/?access_token=%s") % ACCESS_TOKEN


def main():
    print "Welcome to InstaBot > "
    ans = True
    while ans:
        print """
                1.Search by user 
                2.Get someone's last post
                3.Exit
                """
        ans = raw_input("What would you like to do ? ")
        if ans == "1":
            search_user()
        elif ans == "2":
            get_post()
        elif ans == "3":
            exit()
        elif ans != "":
            print "Invalid choice... try again!"


def get_post():
    user_id = DATA[0]
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print "fetching data of user : " + DATA[0]
    user_media = req.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Fetch Successful!'
        else:
            print 'Post does not exist!'
    else:
        print "Something went wrong, data fetch error :( "


def self_last_post():
    print "Fetching your last image : "
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % ACCESS_TOKEN
    print 'GET request url : %s' % request_url
    own_media = req.get(request_url).json()     # using name convention from acadview slides/ too lazy to refactor

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Fetch successful!'
        else:
            print 'Post does not exist!'
    else:
        print "Something went wrong, data fetch error :( "


def search_user():
    user = raw_input("Enter Username ")
    search_by_user_url = (BASE_URL + "users/search?q=%s&access_token=%s") % (user, ACCESS_TOKEN)
    data = req.get(search_by_user_url).json()
    if data['meta']['code'] == 200:
        if data:
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)
            f1 = open('data.json')
            data = json.load(f1)
            for item in data:
                if item == 'data':
                    if len(data['data']) > 0:
                        username = data['data'][0]['id']
                        print username
                        DATA.append(username)
                        print "Username " + user + " found with user ID " + DATA[0] + "."
                        # selected_user_menu() >> will show menu for found/selected user
                    else:
                        print "User not found !"
    else:
        print "Something went wrong, data fetch error :( "

main()
