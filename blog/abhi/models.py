
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User 
from django.db.models.base import Model
from django.db.models.fields import AutoField
class Contact(models.Model):
    srno=AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone_no=models.IntegerField()
    issue=models.TextField(max_length=300)
    timestamp=models.DateTimeField(auto_now_add=True,blank=True)
    
    def __str__(self) -> str:
        return 'message from '+self.name+' - '+self.email
class Blogposts(models.Model):
    idno=AutoField(primary_key=True)
    title=models.CharField(max_length=200,default=" ")
    author_name=models.CharField(max_length=120,default=" ")
    subtitle=models.CharField(max_length=200,default=" ")
    content=models.CharField(max_length=12000)
    views=models.IntegerField(default=0)
    likes=models.IntegerField(default=0)
    image=models.ImageField(upload_to="home/images",default="")
    username=models.CharField(max_length=100,default="")
    def __str__(self) -> str:
        return 'blog from '+self.title+' - '+self.subtitle
    class Meta:
        db_table = 'abhi_blogposts'
class BlogComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Blogposts,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)

