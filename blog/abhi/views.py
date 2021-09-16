from django.db.models import query
from django.http import request
from django.shortcuts import redirect, render,HttpResponse
from . models import Contact,Blogposts,BlogComment
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
import os

from django.contrib import messages
def index(request):
    # current_user = request.user
    # print(current_user.first_name)
    blogs=Blogposts.objects.all()
    context={'blogs':blogs}

    return render(request,"home/index.html",context)
def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone_no=request.POST['phone_no']
        issue=request.POST['issue']
        if len(name)>10 and len(issue)>10:
            cont=Contact(name=name,email=email,phone_no=phone_no,issue=issue)
            cont.save()
            messages.success(request,"Success")
    return render(request,"home/contact.html")
def logindof(request):
    if request.method=="POST":
        loginusername=request.POST['username1']
        loginpassword=request.POST['password1']
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request, user)
            return redirect("/")
    return redirect("/loginsignup")
    
        
def signupdof(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['password']
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
    else:
        return HttpResponse("404 page not found")
    return redirect("/loginsignup")
def logoutdof(request):
    logout(request)
    return redirect("/")
def search(request):
    query = request.GET['query']
    if len(query) >80:
        posts=Blogposts.objects.none()
    else:
        posts1=Blogposts.objects.filter(title__icontains=query)
        posts2=Blogposts.objects.filter(content__icontains=query)
        posts=posts1.union(posts2)
    context={'blogs':posts,'query':query}
    return render(request,"home/search.html",context)
def blog(request,title):
    post=Blogposts.objects.filter(title=title).first()
    post.views=post.views+1
    post.save()
    comments=BlogComment.objects.filter(post=post)
    context={'post':post,'comments':comments,'user':request.user}
    return render(request,"home/blogview.html",context)
def bloglikes(request,title):
    post=Blogposts.objects.filter(title=title).first()
    post.likes=post.likes+1
    post.views=post.views-1
    post.save()
    return redirect(f"/blog/{post.title}")
def postcomment(request):
    
    if request.method == 'POST':
            comment=request.POST.get("comment")
            user=request.user
            postidno=request.POST.get("postidno")
            post=Blogposts.objects.get(idno=postidno)
            commentss=BlogComment(comment=comment,user=user,post=post)
            commentss.save()
    return redirect(f"/blog/{post.title}")
print(User)
def loginsignup(request):
    return render(request,"home/loginsignup.html")
def about(request):
    return render(request,"home/about.html")
def myblogs(request):
    return render(request,"home/myblogs.html")
def trending(request):
    return render(request,"home/trending.html")

# Create your views here.
