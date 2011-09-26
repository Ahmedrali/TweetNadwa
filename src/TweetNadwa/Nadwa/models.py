from django.db import models


class Status(models.Model):
    favorited                   = models.BooleanField()                                
    truncated                   = models.BooleanField()
    retweeted                   = models.BooleanField()
    
    retweet_count               = models.IntegerField(null = True)
    
    created_at                  = models.DateTimeField()#auto_now=False, auto_now_add=True
    
    s_id                        = models.CharField(max_length=30, null = True) # id
    in_reply_to_status_id       = models.CharField(max_length=30, null = True)
    in_reply_to_user_id         = models.CharField(max_length=30, null = True)
    
    id_str                      = models.CharField(max_length=200, null = True)
    in_reply_to_status_id_str   = models.CharField(max_length=200, null = True)
    in_reply_to_user_id_str     = models.CharField(max_length=200, null = True)
    
    in_reply_to_screen_name     = models.CharField(max_length=200, null = True)
    contributors                = models.CharField(max_length=200, null = True)
    source                      = models.CharField(max_length=200, null = True)
    text                        = models.CharField(max_length=200, null = True)
    coordinates                 = models.CharField(max_length=200, null = True)
    place                       = models.CharField(max_length=200, null = True)
    geo                         = models.CharField(max_length=200, null = True)
    
    entities                    = models.TextField()
    user                        = models.TextField()
    retweeted_status            = models.TextField()
    
    screen_Name                 = models.CharField(max_length=200, null = True)
    
    nadwa_name = models.CharField(max_length=200, null = False)
    
#    def __unicode__(self):
#        return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s" %(self.favorited, self.in_reply_to_user_id, self.retweeted_status, 
#                                                                               self.contributors, self.source, self.text,
#                                                                               unicode(self.created_at), self.truncated, self.retweeted,
#                                                                               self.in_reply_to_status_id, self.coordinates, self.s_id,
#                                                                               self.entities, self.in_reply_to_status_id_str, self.place,
#                                                                               self.id_str, self.in_reply_to_screen_name, self.retweet_count,
#                                                                               self.geo, self.in_reply_to_user_id_str, self.user
#                                                                               )

class SummaryStatus(models.Model):
    total_RT = models.IntegerField(null = True)
    inside_RT = models.IntegerField(null = True)
    outside_RT = models.IntegerField(null = True)
    
    created_at = models.DateTimeField()
    last_RT_time = models.DateTimeField()
    
    text = models.CharField(max_length=200, null = True)
    screen_name = models.CharField(max_length=200, null = True)
    
    org_id = models.CharField(max_length=30, null = True)
    user_ID = models.CharField(max_length=30, null = True)
    source = models.CharField(max_length=200, null = True)
    
    attendant = models.BooleanField()
    
    interest_time_in_minutes = models.IntegerField(null = True)
    interest_ratio = models.FloatField()
    
    nadwa_name = models.CharField(max_length=200, null = False)
    image = models.CharField(max_length=200, null = True)

#class RetweetUsers(models.Model):
#    org_id = models.CharField(max_length=30, null = True)
#    screen_name = models.CharField(max_length=200, null = True)
#    attendant = models.BooleanField()
#    nadwa_name = models.CharField(max_length=200, null = False)

class Users(models.Model):
    user_ID = models.CharField(max_length=30, null = True, default = '0')
    screen_name = models.CharField(max_length=200, null = True)
    attendant = models.BooleanField(default = True)
    
    nadwa_name = models.CharField(max_length=200, null = False)
    image = models.CharField(max_length=200, null = True)

class Retweets(models.Model):
    org_id = models.CharField(max_length=30, null = True)
    screen_name = models.CharField(max_length=200, null = True)
    user_ID = models.CharField(max_length=30, null = True)
    
class Nadwa(models.Model):
    nadwa_name  = models.CharField(max_length=200, null = False)
    created_at  = models.DateTimeField()