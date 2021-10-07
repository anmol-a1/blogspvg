from re import sub
import re
import uuid
import re
import mysql.connector
from django.db.models import query
from django.http import request
from django.shortcuts import redirect, render,HttpResponse
from . models import Contact,Blogposts,BlogComment
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
import os
from .emails import send_forgot_password_mail

from django.contrib import messages
def index(request):    
    blogs=Blogposts.objects.all()
    posts = sorted(blogs, key=lambda x: x.likes, reverse=True)
    context={'blogs':posts}
    return render(request,"home/index.html",context)
def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone_no=request.POST['phone_no']
        issue=request.POST['issue']
        if len(name)>2 and len(issue)>10:
            cont=Contact(name=name,email=email,phone_no=phone_no,issue=issue)
            cont.save()
            messages.add_message(request, messages.SUCCESS, ' thanks for contacting us, we will try to reach at you ')
        else:
            messages.add_message(request, messages.INFO, 'lenth of name and phone_no must be atleast 3 and 10')

    return render(request,"home/contact.html")
def logindof(request):
    if request.method=="POST":
        loginusername=request.POST['username1']
        loginpassword=request.POST['password1']
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'You logged-in successfully')
            return redirect("/")
        messages.add_message(request, messages.INFO, 'Invalid credetials')
    return redirect("/loginsignup")
    
    
def signupdof(request):
    
    
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        
        pass1=request.POST['password']
        fullname=request.POST['firstname']
        
        
        checkobj=User.objects.filter(username=username).first()
        regex_mail=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        print(checkobj)
        if checkobj is None:
            if len(pass1)<8 or len(fullname)<3:
                messages.add_message(request, messages.INFO, 'length of password and fullname must be atleast 8 and 3 respctively')
                return redirect("/loginsignup")
            if  not re.fullmatch(regex_mail,email):
                messages.add_message(request, messages.INFO, 'Please enter a valid mail')
                return redirect("/loginsignup")
            
            messages.add_message(request, messages.SUCCESS, 'Your registered successfully')
            myuser=User.objects.create_user(username,email,pass1)
            myuser.first_name=fullname
            myuser.save()
            return redirect("/loginsignup")
        messages.add_message(request, messages.INFO, 'username already token try a different one')
        return redirect("/loginsignup")
    else:
        return HttpResponse("404 page not found")
    return redirect("/loginsignup")
def logoutdof(request):
    messages.add_message(request, messages.SUCCESS, 'you logged out successfully')
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
    posts=Blogposts.objects.all()
    posts = sorted(posts, key=lambda x: x.likes, reverse=True)
    print(list(posts))
    return render(request,"home/blogview.html",context)
def trending(request):
    posts=Blogposts.objects.all()
    posts = sorted(posts, key=lambda x: x.likes, reverse=True)
    context={"blogs":posts}
    return render(request,"home/trending.html",context)
def bloglikes(request,title):
    post=Blogposts.objects.filter(title=title).first()
    post.likes=post.likes+1
    post.views=post.views-1
    post.save()
    return redirect(f"/blog/{post.title}")
def postcomment(request):
    
    username = request.user.username
    if request.method == 'POST':
            comment=request.POST.get("comment")
            user=request.user
            print(user)
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
def saveblogpost(request):
    username1=request.user.username
    if request.method == 'POST':
            title=request.POST['title']
            author_name=request.POST['author_name']
            subtitle=request.POST['subtitle']
            content=request.POST['content']
            # image=request.POST['image']
            image=request.FILES['image']
            blogpost=Blogposts(title=title,author_name=author_name,subtitle=subtitle,content=content,image=image,username=username1)
            print(title,author_name,subtitle,content,blogpost,image)
            messages.add_message(request, messages.SUCCESS, 'you successfully uploaded a blog ')
            blogpost.save()
    return redirect("/myblogs")
            

def myblogs(request):
    

    username1=request.user.username
    myblogs=Blogposts.objects.filter(username=username1)
    context={'blogs':myblogs}
    return render(request,"home/myblogs.html",context)
def forgotpassword(request):
    try:
        if request.method=="POST":
            username=request.POST['username']
            if not User.objects.filter(username=username).first():
                print("no user found")
                return redirect('/forgotpassword')
            user_obj=User.objects.get(username=username)
            token=str(uuid.uuid4())
            user_obj.last_name=token
            user_obj.save()
            send_forgot_password_mail(user_obj.email,token)
            messages.add_message(request, messages.SUCCESS, 'we have sent a link to your associated mail ,please check a spam folder')
            return redirect('/loginsignup')
    except Exception as e:
        print(e)
    return render(request,"home/forgotpassword.html")
def changepassword(request,token):

    context={}
    obj=User.objects.filter(last_name=token).first()
    context={'user_id':obj.id,'token':token}
    if request.method=='POST':
        new_password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        userid=request.POST['user_id']
        if userid is None:
            print("User not Found")
            return redirect('/change-password/{token}')
        usobj=User.objects.get(id=userid)
        if new_password==confirm_password:
            messages.add_message(request, messages.SUCCESS, 'you successfully changed a password')
            usobj.set_password(new_password)
            usobj.save()
            return redirect("loginsignup")
        else:
            messages.add_message(request, messages.INFO, 'Passwords not matched')
            return redirect('/change-password/{token}')


        

    return render(request,"home/changepassword.html",context)
# Create your views here.
