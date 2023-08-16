from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from final_exam.easy_drive_reactions.models import Comment

UserModel = get_user_model()


class CustomRegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]
        widgets = {
            "content": forms.TextInput(attrs={'placeholder': 'Comment here!', 'class': 'form-control', 'type': 'text'
                                              , 'id': 'comment-input'})
        }
