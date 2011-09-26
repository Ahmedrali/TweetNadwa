# Create your views here.

from Nadwa.models import *
from django.http import HttpResponse
import datetime
from datetime import timedelta
import threading
import simplejson as json
import math
from django.shortcuts import render_to_response
from jqgridutil import DjangoJqgridUtil
from streamer.StreamThread import StreamThread
from threadController.ThreadController import ThreadController
from TweetNadwa.Nadwa.models import SummaryStatus     

def index(request):
    return render_to_response('index.html')

def createNadwa(request):
    newNadwaName = request.GET.get("nadwaName")
    resp = ""
    exist = isExist(newNadwaName)
    if exist:
        resp = '0'#'existed'
    else:
        streamer = StreamThread()
        streamer.setNadwaName(newNadwaName)
        ThreadController.addNadwa(newNadwaName, streamer)
        nadwa = Nadwa(nadwa_name = newNadwaName, created_at = datetime.datetime.now())
        nadwa.save()
        resp = '1'#'created'
    return HttpResponse(resp)

def syncCreationTime(request):
    nadwaName = request.GET.get("nadwaName")
    res = Nadwa.objects.filter(nadwa_name = nadwaName)
    if len(res) == 1:
        dNadwa = res[0].created_at
        dt = datetime.datetime.now() - dNadwa 
        sec = dt.seconds
        hr = sec / 3600
        sec = sec - (hr * 3600)
        min = sec / 60
        sec = sec - (min * 60)
        t = [hr, min, sec]
    else:
        t = [-1]
    return HttpResponse(json.dumps(t))
        
    
def isExist(nadwaName):
    res = Nadwa.objects.filter(nadwa_name = nadwaName)
    if len(res) == 1:
        return True
    return False

def clearDB(nadwaName):
    SummaryStatus.objects.filter(nadwa_name = nadwaName).delete()
    Status.objects.filter(nadwa_name = nadwaName).delete()
    Users.objects.filter(nadwa_name = nadwaName).delete()
    Nadwa.objects.filter(nadwa_name = nadwaName).delete()

def startTracking(request):
    nadwaName = request.GET.get("nadwaName")
    resp = "" 
    exist = isExist(nadwaName)
    if exist:
        running = ThreadController.isRunning(nadwaName)
        if running:
            resp = '2'#"%s is already running" %nadwaName
        else:
            ThreadController.startNadwa(nadwaName)
            resp = '1'#"#%s is running now" %nadwaName
    else:
        resp = "0" #Nadwa Doesn't Exist. please create your Nadwa
    print 'Start Resp = %s' %resp
    return HttpResponse(resp)

def stopTracking(request):
    nadwaName = request.GET.get("nadwaName")
    owner = request.GET.get("owner")
    if (owner == '0'):
        return HttpResponse('2')
    resp = "" 
    exist = isExist(nadwaName)
    if exist:
        ThreadController.stopNadwa(nadwaName)
        clearDB(nadwaName)
        ThreadController.deleteNadwa(nadwaName)
        resp = '1'#"%s is stopped" %nadwaName
    else:
        resp = '0'#"Nadwa Doesn't Exist. please create your Nadwa"
    print 'Stop Resp = %s' %resp
    return HttpResponse(resp)

def pauseTracking(request):
    nadwaName = request.GET.get("nadwaName")
    resp = ""
    exist = isExist(nadwaName)
    if exist:
        running = ThreadController.isRunning(nadwaName)
        if running:
            ThreadController.pauseNadwa(nadwaName)
            resp = '1'#"%s is Paused" %nadwaName
        else:
            resp = '2'#"#%s didn't start yet" %nadwaName
    else:
        resp = '0'#"Nadwa Doesn't Exist. please create your Nadwa"
    print 'Pause Resp = %s' %resp
    return HttpResponse(resp)

def resumeTracking(request):
    nadwaName = request.GET.get("nadwaName")
    resp = ""
    exist = isExist(nadwaName)
    if exist:
        running = ThreadController.isRunning(nadwaName)
        if running:
            paused = ThreadController.isPaused(nadwaName)
            if paused:
                ThreadController.resumeNadwa(nadwaName)
                resp = '1'#"%s is resumed, and running now..." %nadwaName
            else:
                resp = '2'#"%s is already running..." %nadwaName
        else:
            resp = '3'#"#%s didn't start yet" %nadwaName
    else:
        resp = '0'#"Nadwa Doesn't Exist. please create your Nadwa"
    print 'Resume Resp = %s' %resp
    return HttpResponse(resp)
    
def addUser(request):
    screen_name = request.GET.get("user", None)
    nadwa_name = request.GET.get("nadwaName", None)
    if(screen_name != None):
        user = Users.objects.filter(screen_name = screen_name)
        if len(user) > 0:
            user = user[0]
            user.attendant = True
        else:
            user = Users()
            user.user_ID = 0
            user.screen_name = screen_name
            user.nadwa_name = nadwa_name
            user.attendant = True
        user.save()
    usersCount = Users.objects.count()
    return HttpResponse(usersCount)

def clearUsers(request):
    nadwaName = request.GET.get("nadwaName", None)
    Users.objects.filter(nadwa_name = nadwaName).delete() # Delete all Previous Status
    return HttpResponse("ok")

###########USER TABLE VIEWS###############

def jsUsers(request):
    grid = DjangoJqgridUtil.Jqgrid(Users, displayList = ['screen_name', 'attendant'])
    res = grid.javaScript(request, multiSelect = 'true', rowList = [25, 50, 75], displayList = ['screen_name', 'attendant'], width = 600, cols_width = [0, 300, 300])
    return HttpResponse(res)

def handlerUsers(request):
    grid = DjangoJqgridUtil.Jqgrid(Users, displayList = ['screen_name', 'attendant'])
    res = grid.handler(request)
    return HttpResponse(json.dumps(res))

def editHandlerUsers(request):
    grid = DjangoJqgridUtil.Jqgrid(Users, displayList = ['screen_name', 'attendant'])
    res = grid.editHandler(request)
    return HttpResponse(res)
##########################################

###########USER TABLE VIEWS###############

def jsTweets(request):
    grid = DjangoJqgridUtil.Jqgrid(SummaryStatus, displayList = ['inside_RT', 'outside_RT', 'text', 'screen_name', 'attendant', 'image'])
    res = grid.javaScript(request, multiSelect = 'false', rowList = [25, 50, 75], displayList = ['inside_RT', 'outside_RT', 'text', 'screen_name', 'attendant', 'image'], width = 1050, cols_width = [0, 110, 120, 400, 115, 70, 55])
    return HttpResponse(res)

def handlerTweets(request):
    grid = DjangoJqgridUtil.Jqgrid(SummaryStatus, displayList = ['inside_RT', 'outside_RT', 'text', 'screen_name', 'attendant', 'image'])
    res = grid.handler(request)
    return HttpResponse(json.dumps(res))

def editHandlerTweets(request):
    grid = DjangoJqgridUtil.Jqgrid(SummaryStatus, displayList = ['inside_RT', 'outside_RT', 'text', 'screen_name', 'attendant', 'image'])
    res = grid.editHandler(request)
    return HttpResponse(res)
##########################################

def liveBoard(request):
    lastID = request.GET.get("lastID")
    nadwaName = request.GET.get("nadwaName")
    status = SummaryStatus.objects.filter(nadwa_name = nadwaName).filter(id__gt = lastID)
    res = []
    for st in status:
        tmp = [st.screen_name, st.text, st.attendant, st.image, st.org_id]
        res.append(tmp)
    #Append lastID as record
    if len(status) > 0:
        tmp = [status[len(status)-1].id, 0, 0, 0]
        res.append(tmp)
    return HttpResponse(json.dumps(res))

def getTopTenInside(request):
    nadwaName = request.GET.get("nadwaName", None)
    date = request.GET.get("date", None)
    res = []
    status = SummaryStatus.objects.filter(nadwa_name = nadwaName)
    if date == 'No':
        status = status.order_by('-inside_RT')[0:10]
    else:
        status = status.filter(created_at__gte = date).order_by('-inside_RT')[0:10]
    for st in status:
        tmp = [st.inside_RT, st.screen_name, st.text, st.attendant, st.image]
        res.append(tmp)
    return HttpResponse(json.dumps(res))

def getTopTenOutside(request):
    nadwaName = request.GET.get("nadwaName", None)
    date = request.GET.get("date", None)
    res = []
    status = SummaryStatus.objects.filter(nadwa_name = nadwaName)
    if date == 'No':
        status = status.order_by('-outside_RT')[0:10]
    else:
        status = status.filter(created_at__gte = date).order_by('-outside_RT')[0:10]
    for st in status:
        tmp = [st.outside_RT, st.screen_name, st.text, st.attendant, st.image]
        res.append(tmp)
    return HttpResponse(json.dumps(res))

def getTopTenTotal(request):
    nadwaName = request.GET.get("nadwaName", None)
    date = request.GET.get("date", None)
    res = []
    status = SummaryStatus.objects.filter(nadwa_name = nadwaName)
    if date == 'No':
        status = status.order_by('-total_RT')[0:10]
    else:
        status = status.filter(created_at__gte = date).order_by('-total_RT')[0:10]
    for st in status:
        tmp = [st.total_RT, st.screen_name, st.text, st.attendant, st.image]
        res.append(tmp)
    return HttpResponse(json.dumps(res))

def getTopTenLongestRTTime(request):
    nadwaName = request.GET.get("nadwaName", None)
    date = request.GET.get("date", None)
    res = []
    status = SummaryStatus.objects.filter(nadwa_name = nadwaName)
    if date == 'No':
        status = status.order_by('-interest_time_in_minutes')[0:10]
    else:
        status = status.filter(created_at__gte = date).order_by('-interest_time_in_minutes')[0:10]
    for st in status:
        tmp = [st.interest_time_in_minutes, st.screen_name, st.text, st.attendant, st.image]
        res.append(tmp)
    return HttpResponse(json.dumps(res))

def clearStatus(request):
    nadwaName = request.GET.get("nadwaName", None)
    Status.objects.filter(nadwa_name = nadwaName).delete() # Delete all Previous Status
    SummaryStatus.objects.filter(nadwa_name = nadwaName).delete() # Delete all Previous Summary Status
    return HttpResponse("ok")

def saveStatus(request):
#    print "***** receive Request to save - Stream"
    
    nadwaName = request.POST.get('nadwaName', None)
    s_id = request.POST.get('id', None)
    source = request.POST.get('source','not found')
    text = request.POST.get('text','not found')
    user = request.POST.get('user', None)
    entities = request.POST.get('entities',None)
    retweeted_status = request.POST.get('retweeted_status', "Not Found")
    create_date = request.POST.get('created_at', None)
    
    
    if(create_date == None):
        create_date = datetime.datetime.now()
    else:
        create_date = parseDateTime(create_date)
        
    status = Status()
    status.nadwa_name = nadwaName
    status.favorited = request.POST.get('favorited',False)
    status.truncated = request.POST.get('truncated',False)
    status.retweeted = request.POST.get('retweeted',False)
    status.retweet_count = request.POST.get('retweet_count', '0').replace('+','')
    status.created_at = create_date
    status.s_id = s_id
    status.in_reply_to_user_id = request.POST.get('in_reply_to_user_id', None)
    status.in_reply_to_status_id = request.POST.get('in_reply_to_status_id', None)
    status.id_str = request.POST.get('id_str','not found')
    status.in_reply_to_user_id_str = request.POST.get('in_reply_to_user_id_str','not found')
    status.in_reply_to_status_id_str = request.POST.get('in_reply_to_status_id_str','not found')
    status.contributors = request.POST.get('contributors','not found')
    status.source = source
    status.text = text
    status.coordinates = request.POST.get('coordinates','not found')
    status.place = request.POST.get('place','not found')
    status.in_reply_to_screen_name = request.POST.get('in_reply_to_screen_name','not found')
    status.geo = request.POST.get('geo','not found')
    status.entities = entities
    status.user = user
    status.retweeted_status = retweeted_status

    userId = user[user.find("u'id'")+7:user.find(',', user.find("u'id'"))]
    userName = user[user.find("u'screen_name'")+18:user.find(',', user.find("u'screen_name'"))-1]
#    print "UserId = %s And Screen Name = %s" %(userId, userName)
    status.screen_Name = userName
    status.save();

    if retweeted_status == 'Not Found':
#        print "RT Not Found"
        
        attendant = False
        # add User if not Exist in DB or Adjust UserID if Exist
        user = Users.objects.filter(screen_name = userName)
#        print "Length User = %s" %len(user)
        if len(user) > 0:
#            print "InSide User"
            user = user[0]
            if user.user_ID == 0:
                user.user_ID = userId
                user.save()
            attendant = user.attendant
        else:
#            print "OutSide User"
            user = Users()
            user.user_ID = userId
            user.screen_name = userName
            user.attendant = False
            user.nadwa_name = nadwaName
            user.save()
        profile_image_url = request.POST.get('profile_image_url')
#        print 'profile_image_url = %s ' %profile_image_url
        saveSummaryStatus(0, 0, 0, create_date, create_date, text, userName, s_id, userId, source, attendant, nadwaName, profile_image_url)
    else:
#        print "RT Found"
#        tweetID = retweeted_status[retweeted_status.rfind("u'id_str'") + 13:retweeted_status.rfind("u'id_str'") + 13 + 17]
        tweetID = request.POST.get('status_id')
#        print "Tweet ID = %s" %tweetID
        
        tweet = SummaryStatus.objects.filter(org_id = tweetID)
        
        if len(tweet) > 0:
#            print "Found The Tweet"
            tweet = tweet[0]
            tweet.last_RT_time = create_date
            userRT = Users.objects.filter(screen_name = userName)
#            print "Length userRT = %s" %len(userRT)
            if len(userRT) > 0:
                userRT = userRT[0]
                if userRT.attendant:
#                    print "Inside User"
                    tweet.inside_RT = tweet.inside_RT + 1
                    userRT.user_ID = userId
                    userRT.save()
                else:
#                    print "Outside User"
                    tweet.outside_RT = tweet.outside_RT + 1
            else:
#                print "Outside User"
                tweet.outside_RT = tweet.outside_RT + 1
#                print "Save OutSide User"
                user = Users()
                user.user_ID = userId
                user.screen_name = userName
                user.attendant = False
                user.nadwa_name = nadwaName
                user.save()
#                print "OutSide User Saved"
            tweet.total_RT = tweet.total_RT + 1
            
            interest_time = (tweet.last_RT_time - tweet.created_at)
            tweet.interest_time_in_minutes = int(math.ceil(interest_time.seconds / 60) )
            tweet.interest_ratio = tweet.interest_time_in_minutes  / float(tweet.total_RT)
            
            tweet.save()
#            print "RT Saved"
            retweets = Retweets()
            retweets.org_id = tweetID
            retweets.screen_name = userName
            retweets.user_ID = userId
            retweets.save()
        else:
            pass
#            print "didn't found the tweet"
#    print "Numer of Saved SummaryStatues = %s" %(SummaryStatus.objects.count())
    return HttpResponse("ok")

def prepareString(str):
    import re
    str = str.replace("':", '":')
    str = str.replace("', ", '", ')
    str = str.replace("'}", '"}')
    str = str.replace("u'", '"')
#    str = str.replace("'", '')
    str = str.replace('\\r', '')
    str = re.sub(r'[0-9]L,', ',', str)
    str = str.replace('None', '-1')
    str = str.replace('True', '"True"')
    str = str.replace('False', '"False"')
    return str.encode('latin-1')

def saveSummaryStatus(total_RT, inside_RT, outside_RT, create_date, last_RT_time, text, userName, s_id, userId, source, attendant, nadwaName, profile_image_url):
    summaryStatus = SummaryStatus();
    summaryStatus.total_RT = total_RT
    summaryStatus.inside_RT = inside_RT
    summaryStatus.outside_RT = outside_RT
    
    summaryStatus.created_at = create_date
    summaryStatus.last_RT_time = last_RT_time
    
    summaryStatus.text = text
    summaryStatus.screen_name = userName
    summaryStatus.org_id = s_id
    summaryStatus.user_ID = userId
    summaryStatus.source = source
    summaryStatus.attendant = attendant
    
    summaryStatus.interest_time_in_minutes = 0
    summaryStatus.interest_ratio = 0
    
    summaryStatus.nadwa_name = nadwaName
    summaryStatus.image = '<img class="userimage" width="48" height="48" src=%s />' %profile_image_url
    summaryStatus.save()

def parseDateTime(d):
    s = d.split(" ")
    
    t = s[3].split(":")
    months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun': 6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    y = int(s[5])
    m = int(months[s[1]])
    d = int(s[2])
    h = int(t[0])
    min = int(t[1])
    sec = int(t[2])
    date_time = datetime.datetime(y, m, d, h, min, sec)
    date_time = date_time + timedelta(hours = 2)
    return date_time