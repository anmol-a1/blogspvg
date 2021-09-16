from django.contrib import admin
from .models import Contact,Blogposts,BlogComment
admin.site.register(Contact)
admin.site.register(Blogposts)
admin.site.register(BlogComment)