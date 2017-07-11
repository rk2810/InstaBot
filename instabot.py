# imports
import requests as req
import json
import urllib
from access_token import *  # Import Access token
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# general variables
BASE_URL = "https://api.instagram.com/v1/"
# access token is a confidential thing, So I import it from a file I won't upload on GitHub till last submission day

DATA = []
current_media = []

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
                2.Fetch your info
                3.Exit
                """
        ans = raw_input("What would you like to do ? ")
        if ans == "1":
            search_user()    # make an inline menu
        elif ans == "2":
            fetch_self_menu()
        elif ans == "3":
            print "Exiting !"
            exit()
        elif ans != "":
            print "Invalid choice... try again!"


def fetch_self_menu():
    ans = True
    while ans:
        print """
                        1.Your info 
                        2.Your recent post
                        3.Exit
                        """
        ans = raw_input("What would you like to do ? ")
        if ans == "1":
            self_info()
        elif ans == "2":
            fetch_self_media()
        elif ans == "3":
            print "Exiting !"
            exit()
        elif ans != "":
            print "Invalid choice... try again!"


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % ACCESS_TOKEN
    user_info = req.get(request_url).json()
    if user_info:
        with open('user_info.json', 'w') as outfile:
            json.dump(user_info, outfile)
            f1 = open('user_info.json')

        user_info = json.load(f1)
        for item in user_info:
            if item == 'data':
                user_id = user_info['data']['id']
                user_name = user_info['data']['username']
                print "Username : " + user_name
                print "User ID : " + user_id


def search_user_menu():
    ans = True
    while ans:
        print """
                    1.Fetch recent post 
                    2.Like/Unlike recent post
                    3.Exit
                    """
        ans = raw_input("What would you like to do ? ")
        if ans == "1":
            fetch_media()
        elif ans == "2":
            like_unlike()
        elif ans == "3":
            print "Exiting !"
            exit()
        elif ans != "":
            print "Invalid choice... try again!"


def like_unlike():
    fetch_media()
    media_id = current_media[0]
    quest = int(raw_input('Select what do you want to do:\n'
                          '1. Get no of likes on recent post.\n'
                          '2. Like post.\n'
                          '3. Remove like from a post\n'))
    if quest == 1:
        print "Post by: %s has: %s likes" % (DATA[1], current_media[1])
    if quest == 2:
        request_url = (BASE_URL + 'media/%s/likes') % media_id
        payload = {"access_token": ACCESS_TOKEN}
        post_a_like = req.post(request_url, payload).json()
        if post_a_like['meta']['code'] == 200:
            print 'Successfully liked media'
    if quest == 3:
        request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, ACCESS_TOKEN)
        payload = {"access_token": ACCESS_TOKEN}
        delete_a_like = req.delete(request_url).json()
        if delete_a_like['meta']['code'] == 200:
            print 'Successfully removed like from post'


def post_comments():
    media_id = current_media[0]

    quest = int(raw_input('Select what do you want to do:\n'
                          '1. Comment on recent media.\n'
                          '2. Delete a negative comment.\n'))

    if quest == 1:
        comment = raw_input("Enter 'comment' you want to post")
        payload = {"access_token": ACCESS_TOKEN, 'text': comment}
        request_url = (BASE_URL + 'media/%s/comments') % media_id
        print current_media[0]
        post_comment = req.post(request_url, payload).json()
        if post_comment['meta']['code'] == 200:
            print 'Successfully commented on media'
        else:
            print 'Unable to comment: Try again'

    if quest == 2:
        request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
        get_comment = req.get(request_url).json()
        print get_comment
        if get_comment['meta']['code'] == 200:
            if get_comment['meta']['code'] == 200:
                if len(get_comment['data']):
                    for x in range(0, len(get_comment['data'])):

                        comment_id = get_comment['data'][x]['id']
                        comment_text = get_comment['data'][x]['text']
                        print comment_id
                        blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                        if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                            print 'Negative comment : %s' % (comment_text)
                            delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id,
                                                                                                 ACCESS_TOKEN)
                            delete_info = req.delete(delete_url).json()

                            if delete_info['meta']['code'] == 200:
                                print 'Negative comment successfully deleted'
                            else:
                                print 'Unable to delete comment'
                        else:
                            print 'No negative comment'
                else:
                    print 'There are no existing comments on the post'
            else:
                print 'Status code other than 200 recieved'


def fetch_media():
    id = DATA[0]

    request_url = (BASE_URL + "users/%s/media/recent?access_token=%s") % (id, ACCESS_TOKEN)
    media = req.get(request_url).json()
    if media:
        with open('recent_media.json', 'w') as outfile2:
            json.dump(media, outfile2)
            f1 = open('recent_media.json')
        media = json.load(f1)
        for item in range(0, 1):
            media_ID = media['data'][item]['id']
            current_media.append(media_ID)
            media_link = media['data'][item]['link']
            media_type = media['data'][item]['type']
            media_likes = media['data'][item]['likes']['count']
            current_media.append(media_likes)
            media_user_like = media['data'][item]['user_has_liked']
            print "Media ID : " + str(media_ID)
            print "Media Link : " + str(media_link)
            print " Media type : " + media_type
            print "Total likes : " + str(media_likes)
            print "Liked by you : " + str(media_user_like)


def fetch_self_media():
    print "Fetching your last image : "
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % ACCESS_TOKEN
    own_media = req.get(request_url).json()  # using name convention from acadview slides/ too lazy to refactor

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
            search_user_menu()
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
                        DATA.append(user)
                        print "Username " + user + " found with user ID " + DATA[0] + "."
                        search_user_menu()
                    else:
                        print "User not found !"
    else:
        print "Something went wrong, data fetch error :( "

main()
