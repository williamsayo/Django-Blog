from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, EmailField
from django.urls import reverse
from django.utils import timezone
import datetime
from django.db.models import Q

class PostManager(models.Manager):
    def search(self , q_search = None):

        post = self.get_queryset()
        if q_search is not None:

            author_search = User.objects.filter(username__icontains=q_search)[:1]
            post_search = (Q(title__icontains = q_search) | Q(category__icontains = q_search) | Q(author = author_search))

            post = post.filter(post_search)

        return post


class Post(models.Model):
    categories = (('WORLD','WORLD'),('TECHNOLOGY','TECHNOLOGY'),('DESIGN','DESIGN'),('BUSSINESS','BUSSINESS'),('POLITICS','POLITICS'),
            ('HEALTH','HEALTH'),('TRAVEL','TRAVEL'))
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    date_posted = models.DateTimeField(default=timezone.now)
    summary = models.CharField(max_length=150,blank=True,null=True)
    content = models.TextField()
    category = models.CharField(max_length=40,choices=categories)
    post_image = models.ImageField(upload_to='post_pic',blank=True,null=True)
    
    objects = PostManager()

    def __str__(self):
        return self.title

    def post_summary(self):
        return self.content[:200]

    def get_absolute_url(self):
        return reverse('view-post',kwargs={'pk':self.pk})

    def comments_quantity(self):
        amount = Comments.objects.filter(post_comment=self.pk)
        return amount
        

    def month_ago(self):
        today = datetime.datetime.now()
        date_str = self.date_posted.strftime('%m,%d,%Y')
        date_obj = datetime.datetime.strptime(date_str,'%m,%d,%Y')
        amnt_days = today - date_obj
        if amnt_days.days > 30:
            months = amnt_days.days/30
            months = int(months)
            return str(months) + ' months ago'

        elif amnt_days.days == 0:
            return 'Today'

        else:
            if amnt_days.days < 2:
                return str(amnt_days.days) + ' day ago'
            else:
                return str(amnt_days.days) + ' days ago'

class FeaturedPost(models.Model):
    featured = models.ForeignKey(Post,on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.featured.title
    

class Comments(models.Model):
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('view-post',kwargs={'pk':self.pk})

class Subscriber(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    time_stamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

