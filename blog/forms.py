from django import forms
from .models import Posts
from .models import Comment


class PostsForm(forms.ModelForm):
    class Meta:
        widgets = {}
        model = Posts
        path = forms.CharField(required=False)
        fields = {'title','category','description','picture','pic_name' }
        widgets = {
            'picture': forms.HiddenInput(),
            'pic_name': forms.HiddenInput(),
            'title' : forms.TextInput(attrs={'style': 'border-color:darkgoldenrod; border-radius: 35px;', 'placeholder':'หัวข้อโพสต์'})
            
            }
        labels = {
            'title':'',
            'category':'',
            'description':'',
            
        }
        
    description = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'รายละเอียด',
        'rows':3,
       
    }))
  
   
   



class CommentForm(forms.ModelForm):
    class Meta:
        
        widgets = {}
        model = Comment
        fields = {'content','picture','pic_name'}
        widgets = {'picture': forms.HiddenInput(),'pic_name': forms.HiddenInput()}

    content = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Comment ',
        'rows':5,
        'cols':9,
    }))
  
   