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
        print(email)
        print(email2)
        print(self.cleaned_data)
        if email != email2:
            raise forms.ValidationError("The emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("The emails has already been register")
        return email
