from django import forms
from .models import Posts

class PostsForm(forms.ModelForm):
    class Meta:
        widgets = {}
        model = Posts
        fields = {'title','category','description' , 'picture' ,'pic_name' }
        widgets = {'picture': forms.HiddenInput(),'pic_name': forms.HiddenInput()}

       
    

   
