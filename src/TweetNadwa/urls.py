from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('Nadwa.views',                 
    
    (r'^req$', 'requestToken'),
    (r'^respToken$', 'respToken'),
                  
    (r'^$', 'index'),
    (r'^/$', 'index'),
    (r'^index$', 'index'),
    
    (r'^createNadwa$', 'createNadwa'),
    
    (r'^startTracking$', 'startTracking'),
    (r'^pauseTracking$', 'pauseTracking'),
    
    (r'^resumeTracking$', 'resumeTracking'),
    (r'^stopTracking$', 'stopTracking'),
    
    (r'^syncCreationTime$', 'syncCreationTime'),
    
    (r'^liveBoard$', 'liveBoard'),
    (r'^topLiveBoard$', 'topLiveBoard'),
    
    (r'^jsUsers$', 'jsUsers'),
    (r'^handlerUsers/$', 'handlerUsers'),
    (r'^editHandlerUsers/$', 'editHandlerUsers'),
    
    (r'^jsTweets$', 'jsTweets'),
    (r'^handlerTweets/$', 'handlerTweets'),
    (r'^editHandlerTweets/$', 'editHandlerTweets'),
    
    (r'^getTopTenInside$', 'getTopTenInside'),
    (r'^getTopTenOutside$', 'getTopTenOutside'),
    (r'^getTopTenTotal$', 'getTopTenTotal'),
    (r'^getTopTenLongestRTTime$', 'getTopTenLongestRTTime'),
    
    (r'^addUser$', 'addUser'),
    
    (r'^clearUsers$', 'clearUsers'),
    (r'^clearStatus$', 'clearStatus'),
    
    (r'^saveStatus$', 'saveStatus'),
    (r'^admin/', include(admin.site.urls)),
)
