import tweetstream
import anyjson
import simplejson as json
import sqlite3
import os
import urllib, urllib2
from datetime import *
import math
#['favorited', 'in_reply_to_user_id', 'retweeted_status', 'contributors', 'source', 'text', 'created_at', 'truncated', 'retweeted', 'in_reply_to_status_id', 'coordinates', 'id', 'entities', 'in_reply_to_status_id_str', 'place', 'id_str', 'in_reply_to_screen_name', 'retweet_count', 'geo', 'in_reply_to_user_id_str', 'user']




def run():
#	track = "tahrir"
	track = "TestNadwa"
	q = "q=%s&result_type=mixed&rpp=50" %track
	url = "http://search.twitter.com/search.json?%s" %q
	dNow = datetime.now() - timedelta(hours=2)
	done = False
	while url != None:
		stream = openConn(url)
		from django.utils.encoding import smart_str, smart_unicode
		data = stream.readline()
		data = anyjson.deserialize(data)
		unData = {}
		for k,v in data.items():
			print "-- %s --"%(k)
			if (k == "results"):
				for n in range(len(v)):
					status = v[n]
					for key,val in status.items():
						if(key == "created_at"):
							dStatus = parseDateTimeSearch(val)
							
							print "dStatus = %s" %dStatus
							print "dNow = %s" %dNow
							dDiffH = dNow.hour - dStatus.hour
#							dDiff = dNow.minute - dStatus.minute
							dDiff = dNow - dStatus
							print "dDiff = %s " %(dDiff.seconds)
#							if( dNow.day != dStatus.day or math.fabs(dDiffH) > 2 or dDiff > 50 ): # 5 Min
							if(math.fabs(dDiff.seconds > 3000)): # 5 Min
								print "Done"
								done = True
								break;
						unData[key] = smart_str(val)
					if(done):
						print "Done"
						break;
					params = urllib.urlencode(unData)
					f = urllib.urlopen('http://127.0.0.1:8000/saveSearchStatus', params)
					d = f.read()
					filename = "err.html"
					file = open(filename, 'w')
					file.write(d)
					file.close()
					f.close()
			else:
				print "-- %s " %smart_str(v)
		if("next_page" in data):
			v = data["next_page"]
			if(done):
				done = False
#				print "Done"
#				url = None
#				break;
			print v
			if(v != None):
				q = smart_str(v)
				url = "http://search.twitter.com/search.json%s" %q
				print "New URl = %s" %url
			else:
				url = None
		else:
			url = None
		print "======================"
		print "======================"

		
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



def openConn(url):
	print """Open the connection to the twitter server"""

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

def parseDateTimeSearch(d): 
    #      0   1  2   3    4        5
    # d = Sat, 16 Jul 2011 20:41:18 +0000
    s = d.split(" ")
    print "Befor split = %s " %str(d)
    print "After split = %s " %s
    
    t = s[4].split(":")
    months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun': 6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    y = int(s[3])
    m = int(months[s[2]])
    d = int(s[1])
    h = int(t[0])
    min = int(t[1])
    sec = int(t[2])
    date_time = datetime(y, m, d, h, min, sec)
    return date_time
run() 
#connect()