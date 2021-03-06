from django.shortcuts import render, redirect
from .forms import PostsForm
import datetime
from .models import Posts
import requests
from django.contrib import messages

from django.shortcuts import  redirect, get_object_or_404 , HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
import random
from random_word import RandomWords

import os
#like

def like(request):
    print('likeeeeee',request.POST.get('action') )
    if request.method == "POST":
        id = int(request.POST.get('post_id'))
        print('post_id',id)
        post = get_object_or_404(Posts, post_id=id)
 
        if post.liked.filter(id=request.user.id).exists():
            post.liked.remove(request.user.id)
            post.like_count -= 1
            post.save()
        else:
            post.liked.add(request.user.id)
            post.like_count += 1
            post.save()

    return redirect('')

def favourite_add(request,id):
    post = get_object_or_404(Posts, post_id=id)
    print('post',post)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user.id)
    else:
        post.favourites.add(request.user.id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




# Create your views here.
def profile(request,id=0):
    posts = Posts.objects.all().order_by('-post_id')
    return render(request,'profile.html',{'posts':posts})

def post_management(request, id=0, catagory_select=""):
    if request.method == "GET":
        foo = os.listdir('blog/static/media')
        # print(random.choice(foo))
        # get post
        if id == 0:
            if catagory_select != "":
                posts = Posts.objects.filter(category=str(catagory_select)).order_by('-post_id')
            else :
                posts = Posts.objects.all().order_by('-post_id')
            randomName = RandomWords().get_random_word()
            randompicture = random.choice(foo)
            form = PostsForm()
            form = PostsForm(initial={'picture': str(randompicture),'pic_name': str(randomName)})
            print(randompicture)

            return render(request,'index.html', {"posts":posts,'form':form})
        else:
            print('testttt')
            # delete post
            post = Posts.objects.get(post_id=id)
            post.delete()
            return redirect('')
    elif request.method == "POST":
        # create post
        form = PostsForm(request.POST)
        # print(form.is_valid())
        # print('form',form)
        if form.is_valid():
            # print('form',form)
            # print(form.instance)
            url = "https://api.aiforthai.in.th/bully"
            text = form.instance
            
            data = {'text':text}
            
            headers = {   
                'Apikey': "vM0LY7YAGqM2DhFbJHI3ON5mmg71vs9K",
                }
            
            response = requests.post(url, data=data, headers=headers)
            print('response')
            print(response.json())
            if (response.json()['bully_type'] != 0):
                print(response.json()['bully_word'] , 'เป็นคำไม่สุภาพกรุณาพิมพ์ให้สุภาพ')            
                messages.warning(request,response.json()['bully_word'])            
                return redirect('')
            else:
                print('บันทึกสำเร็จ')
                print(response.json())
                form.save()
                return redirect('')

def post_update(request, id=0):
    if request.method == "GET":
        post = Posts.objects.get(post_id=id)
        form = PostsForm(instance=post)
        return render(request,'updatepost.html',{'form':form,'id':id})
    elif request.method == "POST":
        post = Posts.objects.get(post_id=id)
        form = PostsForm(request.POST, instance=post)
        if form.is_valid():
            url = "https://api.aiforthai.in.th/ssense"
            text = form
            
            data = {'text':text}
            
            headers = {   
                'Apikey': "vM0LY7YAGqM2DhFbJHI3ON5mmg71vs9K"
                }
            
            response = requests.post(url, data=data, headers=headers)
            result = (response.json()['se-ntiment']['polarity'])
            if (result == 'negative' ):
                print('กรุณาพิมพ์ให้สุภาพ')
                messages.warning(request,'กรุณาพิมพ์ให้สุภาพหรือตามกฏ')            
            else:
                print('บันทึกสำเร็จ')
                print(response.json())
                form.save()
            return redirect('')

#category

def category_love(request):
    posts = Posts.objects.all()
    return render(request,'category_love.html',{"posts":posts})
