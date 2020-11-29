from django import forms
from django.forms import fields
from django.forms import widgets
from .models import Comments,Subscriber

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

class SubscriberForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}),label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email','id':'email'}),label='')
    class Meta:
        model = Subscriber
        fields = ['name','email']