from django import forms
from .models import Posts
from .models import Comment


class PostsForm(forms.ModelForm):
    class Meta:
        widgets = {}
        model = Posts
        path = forms.CharField(required=False)
        fields = {'title','category','description' , 'picture' ,'pic_name' }
        widgets = {'picture': forms.HiddenInput(),'pic_name': forms.HiddenInput()}
        labels = {
            'title':'หัวข้อ',
            'category':'หมวดหมู่',
            'description':'รายละเอียด',
        }
    description = forms.CharField(label ="เนื้อหาข้อความ", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'',
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
  
   