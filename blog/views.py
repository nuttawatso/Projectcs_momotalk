from django.shortcuts import render, redirect
from .forms import PostsForm
import datetime
from .models import Posts
from .models import Comment
import requests
from django.contrib import messages

from django.shortcuts import  redirect, get_object_or_404 , HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
import random
from random_word import RandomWords

import os

from .forms import CommentForm
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
    
#comment
# def comment_add(request, id):
    
#     if request.method == "POST":
#         foo = os.listdir('blog/static/media')
#         if id == 0: 
#             posts = Posts.objects.all()
#             posts.post_comment.add(request.user.id)
#             randomName = RandomWords().get_random_word()
#             randompicture = random.choice(foo)
#             form = PostsForm()
#             form = PostsForm(initial={'picture': str(randompicture),'pic_name': str(randomName)})
#             form = PostsForm(request.POST)
#             form.save()
#         return HttpResponseRedirect(request.META['HTTP_REFERER'])


 

# Create your views here.
def profile(request,id=0):
    posts = Posts.objects.all().order_by('-post_id')
    return render(request,'profile.html',{'posts':posts})

def favourties(request,id=0):
    posts = Posts.objects.all()
    fav_post=[]
    for post in posts:
        if(post.favourites.all().filter(id=request.user.id).exists()):
            fav_post.append(post)
    # posts = posts.favourites.filter(user_id=request.user.id)
    return render(request,'favourties.html',{'posts':fav_post})

def post_comment(request,id=0):
    post = get_object_or_404(Posts, post_id=id)

    all_comments = Comment.objects.filter(post_id=id).order_by("-timestamp")
    if request.method == 'POST':
        foo = os.listdir('blog/static/media')
        cf=CommentForm(request.POST or None)
        if cf.is_valid():
            content=request.POST.get('content')
            url = "https://api.aiforthai.in.th/bully"
            
            data = {'text':content}
            
            headers = {   
                'Apikey': "vM0LY7YAGqM2DhFbJHI3ON5mmg71vs9K",
                }
            
            response = requests.post(url, data=data, headers=headers)
            print('response')
            print(response.json())
            if (response.json()['bully_type'] != 0):
                print(response.json()['bully_word'] , 'เป็นคำไม่สุภาพกรุณาพิมพ์ให้สุภาพ')            
                messages.warning(request,response.json()['bully_word'])            
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                    
                if request.user.id == post.user_id:
                    comment=Comment.objects.create(post=post,user=request.user,content=content,picture=post.picture,pic_name= post.pic_name)
                    print('บันทึกคอมเมนต์ :',comment , 'ชื่อ: ',randomName, 'ภาพ: ',randompicture )
                    comment.save()

                elif Comment.objects.filter(user_id=request.user.id).filter(post_id=id).exists():
                    print(Comment.objects.filter(user_id=request.user.id).filter(post_id=id)[0].picture)
                    chk_user = Comment.objects.filter(user_id=request.user.id).filter(post_id=id)[0]
                    comment=Comment.objects.create(post=post,user=request.user,content=content,picture=chk_user.picture,pic_name= chk_user.pic_name)
                    print('บันทึกคอมเมนต์ :',comment , 'ชื่อ: ',randomName, 'ภาพ: ',randompicture )
                    comment.save()

                else:

                    comment=Comment.objects.create(post=post,user=request.user,content=content,picture=str(randompicture),pic_name= str(randomName))
                    print('บันทึกคอมเมนต์ :',comment , 'ชื่อ: ',randomName, 'ภาพ: ',randompicture )
                    comment.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     
    else:
        cf=CommentForm()

    return render(request,'post_comment.html',{"comments":cf,'all_comments':all_comments,'post':post})

def del_comment(request,id=0):
    if request.method == "GET" and id!=0:
        
        print('testttt')
        # delete post
        post = Comment.objects.get(id=id)
        post.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
def catagory_select(request,  catagory_select=0):
    list_category = ['all','ทั่วไป','ความรัก','ปรึกษา','การเรียน','การเมือง']
    foo = os.listdir('blog/static/media')

    print(list_category[int(catagory_select)])
    catagory_select = int(catagory_select)
    if catagory_select != 0:
        posts = Posts.objects.filter(category=list_category[catagory_select]).order_by('-post_id')
        hotPosts = Posts.objects.filter(category=list_category[catagory_select]).order_by('-like_count')
        randomName = RandomWords().get_random_word()
        randompicture = random.choice(foo)
        form = PostsForm()
        form = PostsForm(initial={'picture': str(randompicture),'pic_name': str(randomName)})
    return render(request,'index.html', {"posts":posts,'form':form,"hotPosts":hotPosts})
    
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
                hotPosts = Posts.objects.all().order_by('-like_count')
                randomName = RandomWords().get_random_word()
                randompicture = random.choice(foo)
                form = PostsForm()
                form = PostsForm(initial={'picture': str(randompicture),'pic_name': str(randomName)})
                print(randompicture)

            return render(request,'index.html', {"posts":posts,'form':form,"hotPosts":hotPosts})
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
        print(id,'edit')
        post = Posts.objects.get(post_id=id)
        form = PostsForm(request.POST, instance=post)
        print('from ', form.errors)
        if form.is_valid():
            url = "https://api.aiforthai.in.th/bully"
            text = form
            print('check form')
            
            data = {'text':text}
            
            headers = {   
                'Apikey': "vM0LY7YAGqM2DhFbJHI3ON5mmg71vs9K",
                }
            
            response = requests.post(url, data=data, headers=headers)
            if (response.json()['bully_type'] != 0):
                print('กรุณาพิมพ์ให้สุภาพ')
                messages.warning(request,response.json()['bully_word'])  
                return redirect('')          
            else:
                print('บันทึกสำเร็จ')
                print(response.json())
                form.save() 
        return redirect('')

# def update_detail(re)
#category

def category_love(request):
    posts = Posts.objects.all()
    return render(request,'category_love.html',{"posts":posts})
