#!/usr/bin/python

import twitter
import ConfigParser

config_file = "user.cfg"
config = ConfigParser.RawConfigParser()
config.read(config_file)
api = twitter.Api(username=config.get("twitter","username"),password=config.get("twitter","password")  )
    
followers = set(map(lambda x : x.screen_name,api.GetFollowers()))
friends = set(map(lambda x : x.screen_name,api.GetFriends())) 
   
print " Who I follow but not follow me"
for user in friends:
    if user not in followers:
        print " ", user

print " Who follow me but I not follow "
for user in followers:
    if user not in friends:
        print " ", user
