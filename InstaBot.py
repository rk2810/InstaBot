# imports
import requests as req
import json
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


def search_user():
    user = raw_input("Enter Username ")
    search_by_user_url = (BASE_URL + "users/search?q=%s&access_token=%s") % (user, ACCESS_TOKEN)
    data = req.get(search_by_user_url).json()
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
                    exit()


search_user()
