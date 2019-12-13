from django.db import models

# Create your models here.
class Videoinfo(models.Model):
    vid = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    thumbnailurl = models.CharField(max_length=50)
    videourl = models.CharField(max_length=50)
    duration = models.IntegerField()
    description = models.TextField()

class Categoryinfo(models.Model):
    cid = models.CharField(max_length=15)
    cname = models.CharField(max_length=50)


class Mylearninginfo(models.Model):
    userid = models.CharField(max_length=20)
    videoid = models.CharField(max_length=20)
    categoryid = models.CharField(max_length=15)
    categoryname = models.CharField(max_length=50)
