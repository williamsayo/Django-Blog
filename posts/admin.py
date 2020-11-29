from django.contrib import admin
from .models import Post,Comments,FeaturedPost,Subscriber

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','category','content','date_posted']
    list_display_links = ['author','category']
    list_filter = ['author','category']

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['post_comment','comment','comment_author','date_posted']
    list_display_links = ['post_comment','comment_author']
    list_filter = ['comment_author','post_comment']

class FeaturedPostAdmin(admin.ModelAdmin):
    list_display = ['featured']
    list_display_links = ['featured']

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['name','email','time_stamp']

admin.site.register(Post,PostAdmin)

admin.site.register(Comments,CommentsAdmin)

admin.site.register(FeaturedPost,FeaturedPostAdmin)

admin.site.register(Subscriber,SubscriberAdmin)
