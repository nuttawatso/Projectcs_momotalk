from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import crum
#--
from os import listdir
from os.path import join as path_join
import time
#--
# Create your models here.
CATEGORY_CHOICES = (
    ('ทั่วไป', 'ทั่วไป'),
    ('ความรัก', 'ความรัก'),
    ('ปรึกษา', 'ปรึกษา'),
    ('การเรียน', 'การเรียน'),
)



class Posts(models.Model):
    def __str__(self):
        return f'{self.title},{self.description}'
    
    
    def save(self, *args, **kwargs):
        user_id = crum.get_current_user()
        self.user_id = user_id.id

        super(Posts, self).save(*args, **kwargs)

    
    
    
    title = models.CharField(max_length=80) 
    description = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)
    category= models.CharField(max_length=200 ,choices=CATEGORY_CHOICES, default='ทั่วไป')
    user_id = models.IntegerField(blank=True, default=crum.get_current_user())
    post_id = models.AutoField(auto_created = True, primary_key=True)
    picture = models.CharField(max_length=200 , null=True)
    pic_name = models.CharField(max_length=100)
    favourites = models.ManyToManyField(
        User, related_name='favourite', default=None, blank=True)
    liked = models.ManyToManyField(
        User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')

    objects=models.Manager()
      # custom manager

    # @property
    # def num_like(self):
    #     return self.liked.all().count()

# class Like(models.Model):
#     user = models.ForeignKey

class Comment(models.Model):
    description = models.CharField(max_length=50)
    datetime = models.DateTimeField(default=timezone.now)


class Random(models.Model):
    user_id = models.IntegerField(blank=True, default=crum.get_current_user())
    post_id = models.AutoField(auto_created = True, primary_key=True)