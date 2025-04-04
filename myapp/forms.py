from django import forms
from .models import Tasks, Comments, Attachments

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'status', 'priority', 'deadline']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

class AttachmentForm(forms.ModelForm):
    file_url = forms.FileField()  # Use FileField for file uploads

    class Meta:
        model = Attachments
        fields = ['file_url']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


