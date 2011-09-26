'''
Created on Jul 25, 2011

@author: Ahmed H.Ali
'''

import urllib, urllib2
import threading
import anyjson

class StreamThread ( threading.Thread ):
    instance = None
    def __init__ (self):
        threading.Thread.__init__(self)
        self._stopThread = threading.Event()
        self.stopNadwa = False
        self.pauseNadwa = False
        
        self.opener = None
        self.conn = None
        self.newConn = False
        self.running = False
        self.nadwaName = None
        self.stopStream = False
        
    def run ( self ):
        self.running = True
        self.openConn()
        from django.utils.encoding import smart_str, smart_unicode
        while True:
            if self.stopNadwa:
                break;
            if self.pauseNadwa:
                continue;
            data = self.conn.readline()
            if (data != None and data != "" and len(data) > 2):
                data = anyjson.deserialize(data)
                unData = {}
                unData['nadwaName'] = self.nadwaName
                for k,v in data.items():
                    if k == "user":
                        unData['profile_image_url'] = v['profile_image_url']
                    if k == "retweeted_status":
                        unData['status_id'] = v['id_str']
#                        print 'activities_Key = %s ' %(v['activities'])
                    unData[k] = smart_str(v)
                print "======================"
                try:
                    params = urllib.urlencode(unData)
                    f = urllib.urlopen('http://127.0.0.1:8000/saveStatus', params)
                    file = open("./error.html", 'w')
                    file.write(f.read())
                    file.close()
                    code = f.code
                    f.close()
#                    if (code == 500):
#                        break;
                except:
                    pass
        print 'Stopped'
    
    def stop(self):
        self.stopNadwa = True
    
    def isPaused(self):
        return self.pauseNadwa
    
    def resumeTraking(self):
        self.openConn()
        self.pauseNadwa = False
    
    def pauseTracking(self):
        self.pauseNadwa = True
        self.opener.close()
    
    def isRunning(self):
        return self.running
    
    def setNadwaName(self, name):
        self.nadwaName = name
        
    def readNadwaName(self):
        return self.nadwaName
    
    def openConn(self):
        print """Open the connection to the twitter server"""
    
        track = self.readNadwaName()
        url = "http://stream.twitter.com/1/statuses/filter.json?track=%s"%track
        req = urllib2.Request(url, None)
    
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, "TNadwa", "sameh+mohamed")
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        self.opener = urllib2.build_opener(handler)
    
        try:
            self.conn = self.opener.open(req)
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