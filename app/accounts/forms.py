from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-group form-control form-control-user'})
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-group form-control form-control-user'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-group form-control form-control-user', 'placeholder':'Username'})
    )
    email = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-group form-control form-control-user', 'placeholder':'Email'})
    )
    email2 = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-group form-control form-control-user', 'placeholder':'Confirm Email'})
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-group form-control form-control-user', 'placeholder':'Password'}))

    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-group form-control form-control-user', 'placeholder':'Repeat Password'}))


    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
            'password2'
        ]


    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("The emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("The emails has already been register")
        return email

class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-group form-control form-control-user', 'placeholder':'New Username'})
    )
    email = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-group form-control form-control-user', 'placeholder':'New Email'})
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-group form-control form-control-user', 'placeholder':'Password'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
    def __init__(self, user, data=None):
        self.user = user
        super(ProfileForm, self).__init__(data=data)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email=='' and username=='':
            raise forms.ValidationError('Theres nothing to change!')
        if username:
            username_qs = User.objects.filter(username=username)
            if username_qs.exists():
                raise forms.ValidationError('Error this Username already exists!')
        if email:
            email_qs = User.objects.filter(email=email)
            if email_qs.exists():
                raise forms.ValidationError('Error this email already exists!')
        if password:
            if not self.user.check_password(password):
                raise forms.ValidationError('Wrong password')
