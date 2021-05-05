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
from random_word import RandomWords
from django.contrib.auth.decorators import login_required
import os
from .forms import CommentForm
import requests
import random

    
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        exist=0
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Posts, post_id=id)
        # print('trttt',request.POST.get('postid'),post)
        if post.liked.filter(id=request.user.id).exists():
            post.liked.remove(request.user.id)
            post.like_count -= 1
            # print(post.liked,post.like_count)
            result = post.like_count
            exist=0
            post.save()
        else:
            post.liked.add(request.user.id)
            post.like_count += 1
            result = post.like_count
            # print(post.like_count)
            exist=1
            post.save()
        return JsonResponse({'result': result,'postId': id,'exist':exist })

def favourite_add(request):
    if request.POST.get('action') == 'post':    
        id = int(request.POST.get('postid'))
        print('trttt',request.POST.get('postid'))
        post = get_object_or_404(Posts, post_id=id)
        print('post',post)
        if post.favourites.filter(id=request.user.id).exists():
            post.favourites.remove(request.user.id)
            exist=0
        else:
            post.favourites.add(request.user.id)
            exist=1
        return JsonResponse({'postId': id })
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

    

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
    return render(request,'favourties.html',{'posts':fav_post})

def post_comment(request,id=0):
    post = get_object_or_404(Posts, post_id=id)
    all_comments = Comment.objects.filter(post_id=id).order_by("-timestamp")
    if request.method == 'POST':
        foo = os.listdir('blog/static/media')      
        word_site = "https://www.usna.edu/Users/cs/roche/courses/s15si335/proj1/files.php%3Ff=names.txt&downloadcode=yes"
        response = requests.get(word_site)
        WORDS = response.content.splitlines()
        randomName = random.choice(WORDS).decode("utf-8")
        randompicture = random.choice(foo)
        cf=CommentForm(request.POST or None)
        if cf.is_valid():
            content=request.POST.get('content')
            url = "https://api.aiforthai.in.th/bully"   
            data = {'text':content}            
            headers = {   
                'Apikey': "vM0LY7YAGqM2DhFbJHI3ON5mmg71vs9K",
                }          
            response = requests.post(url, data=data, headers=headers)
            # print('response')
            # print(response.json())
            if (response.json()['bully_type'] != 0):
                messages.warning(request,response.json()['bully_word']+['เป็นคำไม่สุภาพ กรุณาแก้ไข'])            
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:   
                if request.user.id == post.user_id:
                    comment=Comment.objects.create(post=post,user=request.user,content=content,picture=post.picture,pic_name= post.pic_name)
                    # print('if')
                    comment.save()
                elif Comment.objects.filter(user_id=request.user.id).filter(post_id=id).exists():
                    # print(Comment.objects.filter(user_id=request.user.id).filter(post_id=id)[0].picture)
                    chk_user = Comment.objects.filter(user_id=request.user.id).filter(post_id=id)[0]
                    # print('elif',chk_user)
                    comment=Comment.objects.create(post=post,user=request.user,content=content,picture=chk_user.picture,pic_name= chk_user.pic_name)
                    comment.save()       
                else:
                    comment=Comment.objects.create(post=post,user=request.user,content=content,picture=str(randompicture),pic_name= str(randomName))
                    print('el')
                    comment.save()       
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        cf=CommentForm()
    return render(request,'post_comment.html',{"comments":cf,'all_comments':all_comments,'post':post})

def del_comment(request,id=0):
    if request.method == "GET" and id!=0:
        # print('testttt')
        post = Comment.objects.get(id=id)
        post.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
def catagory_select(request,  catagory_select=0):
    list_category = ['all','ทั่วไป','ความรัก','ปรึกษา','การเรียน','การเมือง','ดนตรี','นิยาย/ซีรี่ย์']
    foo = os.listdir('blog/static/media')
    # print(list_category[int(catagory_select)])
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
                word_site = "https://www.usna.edu/Users/cs/roche/courses/s15si335/proj1/files.php%3Ff=names.txt&downloadcode=yes"
                response = requests.get(word_site)
                WORDS = response.content.splitlines()
                randomName = random.choice(WORDS).decode("utf-8")
                randompicture = random.choice(foo)
                form = PostsForm()
                form = PostsForm(initial={'picture': str(randompicture),'pic_name': str(randomName)})
                print(randompicture)

            return render(request,'index.html', {"posts":posts,'form':form,"hotPosts":hotPosts})
        else:
            # print('testttt')
            # delete post
            post = Posts.objects.get(post_id=id)
            post.delete()
            return redirect('')
    elif request.method == "POST":
        # create post
        form = PostsForm(request.POST)
        if form.is_valid():
            url = "https://api.aiforthai.in.th/bully"
            text = form.instance           
            data = {'text':text}         
            headers = {   
                'Apikey': "vM0LY7YAGqM2DhFbJHI3ON5mmg71vs9K",
                }     
            response = requests.post(url, data=data, headers=headers)
            # print('response')
            # print(response.json())
            if (response.json()['bully_type'] != 0):
                # print(response.json()['bully_word'] , 'เป็นคำไม่สุภาพกรุณาพิมพ์ให้สุภาพ')            
                messages.warning(request,response.json()['bully_word']+[': เป็นคำไม่เหมาะสม กรุณาแก้ไข'])              
                return redirect('')
            else:
                # print('บันทึกสำเร็จ')
                # print(response.json())
                form.save()
                messages.success(request,'บันทึกโพสต์สำเร็จ')
                return redirect('')

def post_update(request, id=0):
    if request.method == "GET":
        post = Posts.objects.get(post_id=id)
        form = PostsForm(instance=post)
        return render(request,'updatepost.html',{'form':form,'id':id})
    elif request.method == "POST":
        # print(id,'edit')
        post = Posts.objects.get(post_id=id)
        form = PostsForm(request.POST, instance=post)
        # print('from ', form.errors)
        if form.is_valid():
            url = "https://api.aiforthai.in.th/bully"
            text = form
            # print('check form')
            data = {'text':text}           
            headers = {   
                'Apikey': "vM0LY7YAGqM2DhFbJHI3ON5mmg71vs9K",
                } 
            response = requests.post(url, data=data, headers=headers)
            if (response.json()['bully_type'] != 0):
                # print('กรุณาพิมพ์ให้สุภาพ')
                messages.warning(request,response.json()['bully_word'])  
                return redirect('')          
            else:
                # print('บันทึกสำเร็จ')
                # print(response.json())
                form.save() 
        return redirect('')