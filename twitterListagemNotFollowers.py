#!/usr/bin/python

import twitter
import ConfigParser
import getopt
import sys

def help():
	print """
	Usage : script [OPTIONS]
		[-h | --help]			display this message
		[-c | --conf] file.cfg		configuration file
	"""

def main():

	config_file = "user.cfg"

	try:
		opts,args = getopt.getopt(sys.argv[1:],"hc:",["help","conf="])
	except getopt.GetoptError, err:
		print str(err)

	for o, a in opts:
		if o in ("-c", "--conf"):
			config_file = a
		if o in ("-h", "--help"):
			help();
			sys.exit()

	config = ConfigParser.RawConfigParser()
	config.read(config_file)

	api = twitter.Api(username=config.get("twitter","username"),password=config.get("twitter","password")  )

	followers = map(lambda x : x.screen_name,api.GetFollowers())
	friends = map(lambda x : x.screen_name,api.GetFriends())

	print " Who I follow but not follow me"
	for user in friends:
		if user not in followers:
			print " ", user

	print " Who follow me but I not follow "
	for user in followers:
		if user not in friends:
			print " ", user

if __name__ == "__main__":
	main()
