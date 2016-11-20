from django.db import models

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

def create_log(user, type, text):
    log = Log()
    log.user = user
    log.type = type
    log.text = text
    return log

class Type(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

class Log(models.Model):
    user = models.ForeignKey(User)
    type = models.ForeignKey(Type)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s %s' % (self.user, self.type, self.created_time)



