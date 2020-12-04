from django.http import request
from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from itertools import chain
from django.contrib import messages 
from .models import Post,Comments,FeaturedPost, Subscriber
from .forms import CommentForm,SubscriberForm


def Subscribe(request):
    form = SubscriberForm()
    if request.method == "POST":
        form = SubscriberForm(request.POST or None)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            if Subscriber.objects.filter(name=name,email=email).exists():
                form.clean()
                messages.info(request,'You are already subscribed to receive our newsletter')

            else:
                subscriber = Subscriber(name=name,email=email)
                subscriber.save()
                form.clean()
                messages.success(request,'Successfully subscribed to receive our newsletter')

        else:
            form = SubscriberForm()

    return form

class home(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'post'
    ordering = '-date_posted'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest'] = Post.objects.all().order_by('-date_posted')[:3]
        context['featured'] = FeaturedPost.objects.all()
        context['world'] = Post.objects.filter(category='WORLD')
        context['tech'] = Post.objects.filter(category='TECHNOLOGY')
        context['design'] = Post.objects.filter(category='DESIGN')
        context['business'] = Post.objects.filter(category='BUSINESS')
        context['politics'] = Post.objects.filter(category='POLITICS')
        context['health'] = Post.objects.filter(category='HEALTH')
        context['travel'] = Post.objects.filter(category='TRAVEL')
        context['form'] = SubscriberForm()
        
        return context

    def post(self, request, *args, **kwargs):
        Subscribe(self.request)   
        return redirect('/')        

class search(ListView):
    model = Post
    template_name = 'posts/search.html'
    context_object_name = 'post'
    paginate_by = 3

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['search_count'] = self.search_count
        context['search_var'] = self.request.GET['q']
        context['form'] = SubscriberForm()

        return context

    def get_queryset(self):

        request = self.request
        if request.method == 'GET':
            q_search = request.GET['q']

            if q_search is not None:
                post_result = Post.objects.search(q_search)

                post_chain = chain(post_result)

                post = sorted( post_chain,key=lambda instance:instance.pk , reverse=True)

                self.search_count = len(post)

                return post

    def post(self, request, *args, **kwargs):
        Subscribe(self.request)   
        return redirect('/') 
    

class create_post(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content','category','summary','date_posted','post_image']
    template_name = 'posts/new_post.html'
    context_object_name = 'form'
    # success_url = '/'
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def viewpost(request,pk):
    post = Post.objects.get(id=pk)
    comment = Comments.objects.filter(post_comment=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            create_comment = Comments(comment_author=request.user,post_comment=post,comment=form.cleaned_data['comment'])
            create_comment.save()
            form.clean()

            # return redirect('home')
    else:
        form = CommentForm()

    context = {'post':post,'form':form,'comment':comment}

    return render(request,'posts/post_view.html',context)

# class view_post(DetailView):
#     model = Post
#     template_name = 'posts/post_view.html'
#     context_object_name = 'post'

# class comment_post(LoginRequiredMixin,CreateView):
#     model = Comments
#     fields = ['comment']
#     template_name = 'posts/comment_view.html'
#     context_object_name = 'form'
    
#     def form_valid(self,form):
#         form.instance.commentor = self.request.user
#         return super().form_valid(form)

class view_post_by_author(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'post'
    paginate_by = 3

    def get_queryset(self):
        data = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=data).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = get_object_or_404(User,username=self.kwargs.get('username'))
        context['latest'] = Post.objects.filter(author=data).order_by('-date_posted')[:3]
        return context

class view_category(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'post'
    paginate_by = 3

    def get_queryset(self):

        val = self.kwargs.get('category')
        return Post.objects.filter(category=val).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        val = self.kwargs.get('category')
        context['latest'] = Post.objects.filter(category=val).order_by('-date_posted')[:3]
        return context



class update_post(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content','category','summary','date_posted','post_image']
    template_name = 'posts/new_post.html'
    context_object_name = 'form'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class delete_post(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'posts/Delete_post.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# class view_post(DetailView):
#     model = Comments
#     template_name = 'posts/post_view.html'
#     context_object_name = 'post'

def about(request):
    context = {'form':Subscribe(request)}
    return render(request,'posts/about.html',context) 