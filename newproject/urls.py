from django.contrib import admin
from django.conf.urls import url,include
from blog import views
app_name="new"

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # social media
    url(r'^accounts/', include('allauth.urls') ),

    #fav
    url(r'^favourite_add/(?P<id>\d+)',views.favourite_add, name='favourite_add'),
    # post crud
    url(r'^$',views.post_management, name=''),
    url(r'^update-post/(?P<id>\d+)',views.post_update, name='update_post'),
    url(r'(?P<id>\d+)',views.post_management, name='delete_post'),
    url(r'^$',views.post_management, name='catagory_select'),

    # profile
    url(r'^profile',views.profile, name='profile'),

    # like
    url(r'^like/', views.like, name='like'),

    #category
     url(r'category_love/', views.category_love, name='category_love'),





]