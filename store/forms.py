from django import forms

ROLE_CHOICES = (
    ('player', 'Player'),
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

class CreateGameForm(forms.Form):
    game_name = forms.CharField(label="Game Name", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    game_price = forms.FloatField(label="Game Price",
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    game_url = forms.URLField(label="Game URL",
                               widget=forms.URLInput(attrs={'class': 'form-control'}))
    game_category = forms.ChoiceField(label="Game Category",
                              widget=forms.Select(attrs={'class': 'form-control'}), choices=(('No category', 'No category'),
                                                                                                ('Action', 'Action'),
                                                                                                ('Adventure', 'Adventure'),
                                                                                                ('Arcade', 'Arcade'),
                                                                                                ('Music', 'Music'),
                                                                                                ('Platform', 'Platform'),
                                                                                                ('Racing', 'Racing')))
