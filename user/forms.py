from django import forms
from .models import CustomUser, GalleryImage

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65)

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    terms = forms.BooleanField(required=True, error_messages={'required': "You must accept the terms and conditions to complete the registration process."})

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password', 'terms')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)

        if commit:
            user.save()
        
        return user
    
class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'title', 'description']