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



class CommentForm(forms.ModelForm):
    class Meta:
        
        widgets = {}
        model = Comment
        fields = {'content','picture','pic_name'}
        widgets = {'picture': forms.HiddenInput(),'pic_name': forms.HiddenInput()}

    # content = forms.CharField(label ="", widget = forms.Textarea(
    # attrs ={
    #     'class':'form-control',
    #     'placeholder':'Comment here !',
    #     'rows':4,
    #     'cols':50
    # }))
    # class Meta:
    #     model = Comment
    #     fields =['content']
   