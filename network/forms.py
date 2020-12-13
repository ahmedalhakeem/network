from django import forms
from network.models import User, Post
from django.forms import ModelForm

class PostForm(ModelForm):
    class meta:
        model = Post
        fields= ['content', 'timestamp', 'created_by', 'like', 'image']


class PostForm(forms.Form):
    content = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'post-area', 'placeholder': 'enter your post here'}), required=True)
    image = forms.ImageField(label="Upload Image", required=False, widget=forms.FileInput(attrs={'class': 'image-post'}))
    #imestamp = forms.DateTimeField(required=True)
    #created_by = forms.ModelChoiceField(queryset=User.objects.all())
    
    