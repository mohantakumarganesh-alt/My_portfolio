from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Leave a comment...',
                'rows': 3,
                'style': 'background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.1); color: #f8fafc;'
            })
        }
