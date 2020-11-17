from django import forms
from network.models import User, Post
from django.forms import ModelForm

class PostForm(ModelForm):
    class meta:
        model = Post
        fields= ['content', 'timestamp', 'created_by', 'like', 'image']


class PostForm(forms.Form):
    content = forms.CharField(label="write a post", widget=forms.Textarea, required=True)
    #imestamp = forms.DateTimeField(required=True)
    #created_by = forms.ModelChoiceField(queryset=User.objects.all())
    
    