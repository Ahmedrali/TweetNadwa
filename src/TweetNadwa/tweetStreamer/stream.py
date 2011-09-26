import tweetstream
import anyjson
import simplejson as json
import urllib, urllib2

#['favorited', 'in_reply_to_user_id', 'retweeted_status', 'contributors', 'source', 'text', 'created_at', 'truncated', 'retweeted', 'in_reply_to_status_id', 'coordinates', 'id', 'entities', 'in_reply_to_status_id_str', 'place', 'id_str', 'in_reply_to_screen_name', 'retweet_count', 'geo', 'in_reply_to_user_id_str', 'user']

def run():
	stream = openConn()
	from django.utils.encoding import smart_str, smart_unicode
	while True:
		data = stream.readline()
		print "Data = %s" %len(data)
		if (data != None and data != "" and len(data) > 2):
			data = anyjson.deserialize(data)
			unData = {}
			for k,v in data.items():
	#			print "-- %s --"%(k)
	#			v = smart_unicode(v)
	#			print "-- %s " %smart_str(v)
	#			try:
	#				print str(unicode(v))
	#			except:
	#				print "ERRRR" 
				unData[k] = smart_str(v)
			print "======================"
			print "======================"
			params = urllib.urlencode(unData)
			f = urllib.urlopen('http://127.0.0.1:8000/saveStatus', params)
			d = f.read()
	#		print "Data = %s" %(d)
			filename = "err.html"
			file = open(filename, 'w')
			file.write(d)
			file.close()
			f.close()
			
#	print "Run Streamer Now"
#	words = ["onetimeanniversary"]
#	stream = tweetstream.TrackStream("ahmedrali","ahmedbmwz3", words)
##	stream = tweetstream.TrackStream("TNadwa","sameh+mohamed", words)
#	try:
#		for tweet in stream:
#			print tweet.keys()
#			for k,v in tweet.items():
#				print "-- %s --"%(k)
#				try:
#					print str(unicode(v))
#				except:
#					print "ERRRR"
#			print "======================"
#			print "======================"
#			params = urllib.urlencode(tweet)
#			f = urllib2.urlopen('http://127.0.0.1:8000/saveStatus', params)
#			data = f.read()
##			print "Data = %s" %(data) 
#			print data.__dict__
#			f.close()
#	except urllib2.HTTPError, e:
#		print e.code
#		print e.msg
#		print e.headers
#		print e.fp.read()
#		print e.url
#		print e.hdrs

def readNadwaName():
	nadwaName = ''
	file = open("./tweetStreamer/nadwa.txt")
	while 1:
		line = file.readline()
		if not line:
			break
		nadwaName = line
	return nadwaName

def openConn():
	print """Open the connection to the twitter server"""

#	track = "tahrir"
	track = readNadwaName()
	url = "http://stream.twitter.com/1/statuses/filter.json?track=%s"%track
	req = urllib2.Request(url, None)

	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, url, "TNadwa", "sameh+mohamed")
	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)

	try:
		conn = opener.open(req)
		return conn
	except urllib2.HTTPError, e:
		if e.code == 401:
			print("Access denied")
		else: # re raise. No idea what would cause this, so want to know
			print e.code
			print e.msg
			print e.headers
			print e.fp.read()
			print e.url
			print e.hdrs
	except urllib2.URLError, e:
		print e.code
		print e.msg
		print e.headers
		print e.fp.read()
		print e.url
		print e.hdrs
run() 
#connect()