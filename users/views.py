from django.shortcuts import render,redirect
from django.views.generic import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def create_user(request):
    if request.method == 'POST':
        form = NewUser(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'New user created successfully')
            return redirect('login')

    else:
        form = NewUser()

    context = {
        'form':form
    }
    return render(request,'users/new_user.html',context)

# @login_required
# def view_profile(request):
#     if request.method == 'GET':
#         profile = User.objects.all
#         image = Profile.objects.all

class view_profile(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def get_queryset(self):
        data = get_object_or_404(User,username=self.kwargs.get('username'))
        return Profile.objects.filter(user=data)

@login_required
def update_profile(request,username):
    if request.method == 'POST':
        Uform = UpdateUser(request.POST, instance=request.user)
        Pform = UpdateProfile(request.POST, request.FILES, instance=request.user.profile)
        if Uform.is_valid() and Pform.is_valid():
            Uform.save()
            Pform.save()
            messages.success(request,'Profile details updated')
            return redirect('profile-detail', username=request.user.username)

    else:
        Uform = UpdateUser(instance=request.user)
        Pform = UpdateProfile(instance=request.user.profile)

    context = {
        'u_form':Uform,
        'p_form':Pform
    }
    return render(request,'users/profile_view.html',context)
