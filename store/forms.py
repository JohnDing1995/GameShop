from django import forms

ROLE_CHOICES = (
    ('play', 'Player'),
    ('dev', 'Developer')
)

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label="Confirm Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(
        label="I'm a",
        choices=ROLE_CHOICES
    )
    
class LoginForm(forms.Form):

    username = forms.CharField(label="Username", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(
        label="I'm a",
        choices=ROLE_CHOICES

    )