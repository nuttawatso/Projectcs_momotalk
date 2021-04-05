from django.contrib import admin
from django.conf.urls import url,include
from blog import views
app_name="new"

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # social media
    url(r'^accounts/', include('allauth.urls') ),


    #comment_add
    #  url(r'^comment_add/(?P<id>\d+)',views.comment_add, name='comment_add'),
    url(r'^catagory_select/(?P<catagory_select>\d+)/$',views.catagory_select, name='catagory_select'),
    
    #post_comment

    
    url(r'^post_comment/(?P<id>\d+)',views.post_comment, name='post_comment'),
    url(r'^del_comment/(?P<id>\d+)',views.del_comment, name='del_comment'),


    #fav
    url(r'^favourite_add/(?P<id>\d+)',views.favourite_add, name='favourite_add'),
    # post crud
    url(r'^$',views.post_management, name=''),
    # url(r'^$/(?P<categor÷y>\d+)',views.post_management, name=''),
    url(r'^update_post/(?P<id>\d+)',views.post_update, name='update_post'),
    # url(r'(?P<id>\d+)',views.post_comment, name='delete_comment'),
    url(r'(?P<id>\d+)',views.post_management, name='delete_post'),

    # profile
    url(r'^profile',views.profile, name='profile'),

    
    #favourties
    url(r'^favourties',views.favourties, name='favourties'),

    # like 
    url(r'^like/', views.like, name='like'),





    #category
     url(r'category_love/', views.category_love, name='category_love'),





]