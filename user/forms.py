from django import forms
from .models import CustomUser, ProfileReview

class LoginForm(forms.Form):
    username = forms.CharField(max_length=19)
    password = forms.CharField(max_length=65)
    remember_me = forms.BooleanField(required=False)

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    terms = forms.BooleanField(required=True, error_messages={'required': "You must accept the terms and conditions to complete the registration process."})
    username = forms.CharField(
        max_length=19,
        error_messages={
            "max_length": "Username can be up to 19 characters long."
        },
    )

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

class ProfileReviewForm(forms.ModelForm):
    candidate_id = forms.CharField(max_length=100)
    class Meta:
        model = ProfileReview
        fields = ('review', 'candidate_id')