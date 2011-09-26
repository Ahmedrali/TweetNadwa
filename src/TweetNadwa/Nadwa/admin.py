'''
Created on Jan 24, 2011

@author: aali
'''

from Nadwa.models import *
from django.contrib import admin
import datetime
class StausAdmin(admin.ModelAdmin):
    list_display = ('retweet_count',
                    'retweeted',
                    'screen_Name',
                    'favorited', 
                    'truncated', 
                    'created_at',
                    's_id',
                    'in_reply_to_user_id', 
                    'in_reply_to_status_id',
                    'id_str',
                    'in_reply_to_user_id_str',
                    'in_reply_to_status_id_str',
                    'contributors', 
                    'source', 
                    'text',
                    'coordinates',
                    'place', 
                    'in_reply_to_screen_name', 
                    'geo', 
                    'entities', 
                    'user',
                    'retweeted_status',
                    'nadwa_name',
                    )
    
    list_filter = ('retweeted',)
    ordering = ('retweet_count','created_at',)
    search_fields = ('screen_Name',)  
    #actions = [export_as_json]
   

class SummaryStatusAdmin(admin.ModelAdmin):
    list_display = ('total_RT',
                    'inside_RT',
                    'outside_RT',
                    
                    'created_at', 
                    'last_RT_time', 
                    
                    'text',
                    'screen_name',
                    
                    'org_id', 
                    'user_ID',
#                    'source',
                    
                    'attendant',
                    
                    'interest_time_in_minutes',
                    'interest_ratio',
                    
                    'nadwa_name',
                    'image',
                    )
    
#    list_filter = ('attendant',)
    ordering = ('-total_RT', 'inside_RT', 'outside_RT', 'created_at','last_RT_time',)
    search_fields = ['created_at']

    
class UsersAdmin(admin.ModelAdmin):
    list_display = (
#                    'user_ID',
                    'screen_name',
                    'attendant',
                    
                    'nadwa_name',
                    )
    exclude = ('user_ID',)
    list_filter = ('attendant',)
    search_fields = ('screen_name',)

class RetweetsAdmin(admin.ModelAdmin):
    list_display = (
                    'org_id',
                    'screen_name',                    
                    'user_ID',
                    )
    exclude = ('user_ID',)
    search_fields = ('org_id',)

class NadwaAdmin(admin.ModelAdmin):
    list_display = (
                    'nadwa_name',
                    'created_at',
                    )
    search_fields = ('nadwa_name',)
    
admin.site.register(Status, StausAdmin)
admin.site.register(SummaryStatus, SummaryStatusAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Retweets, RetweetsAdmin)
admin.site.register(Nadwa, NadwaAdmin)