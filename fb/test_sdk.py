"""
A simple example script to get all posts on a user's timeline.
Originally created by Mitchell Stewart.
<https://gist.github.com/mylsb/10294040>
"""
import facebook
import requests


def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    print(post)



# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access2_token = 'EAACEdEose0cBACoMAUO4Alp73zPJRglgxwEWt0rqPzenWdKfO0vbA6bLzXOjRdOMq0x6qLsZCJ2ApmPpZC3f63kqkvGksHUqZAZAihY3okckxo0ZB0h7bUBWBFTP8lACNllD1e9LiWQlHyqh6rH5UaCuuRBdqDPG5Cm2NwDHzEnhlc9RlPU1UEZAofUiiMClUZD'
access_token = 'EAACEdEose0cBAAGlmzWtqZCs1P35659WLx6AivMcbyZBJqV5nzPRcnwl8xMryUk3aGDWtXTVYJopzUM9VaX04ntDPZBoGDkW6393eMSn6HWtbSWwaskHBRZCrBXHEjV2BNyxen3ZB0t75qOPbXubyXDmZC0uMPHxiSXr35NTctY1HHbdRTMc3ouvu4s75fFcAZD'
# Look at Bill Gates's profile for this example by using his Facebook id.
user = 'BillGates'

graph = facebook.GraphAPI(access_token=access_token, version='2.1')
# profile = graph.get_object('pavlokach')
#print(profile)
#posts = graph.get_connections(profile['id'], 'posts')
#print(profile['id'], type(profile['id']))
#friends = graph.get_connections('me', 'friends')
#print(friends)
# new = graph.get_object('nazar0romaniv')
permissions = graph.get_connections('me', 'mutualfriends/1077293595718044')
print(permissions)
# print('public_profile' in permissions)
# Wrap this block in a while loop so we can keep paginating requests until
# finished.
while True:
    break
    try:
        # Perform some action on each post in the collection we receive from
        # Facebook.
        [some_action(post=post) for post in posts['data']]
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:

        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break
