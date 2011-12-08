import commands
import logging
import os
import simplejson
import socket
import urllib
import urllib2

import lounge

def getjson(url):
	return simplejson.load(urllib2.urlopen(url))

def main():
	failed = []
	all = getjson("http://lounge:6984/_all_dbs")
	shard_map = lounge.ShardMap()
	for db in all:
		print "Checking", db
		for shard in shard_map.shards(db):
			for url in shard_map.nodes(shard):
				print url
				cmd = 'curl %s' % url
				print cmd
				status, output = commands.getstatusoutput(cmd)
				if status != 0:
					print "failed!", output
					failed.append(url)
	if len(failed)>0:
		print len(failed), "shards failed!"
		for url in failed:
			print url
	else:
		print "All shards present :D"

if __name__ == '__main__':
	main()

	

