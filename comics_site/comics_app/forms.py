from django import forms
from django.forms.utils import ErrorList
from django.db.models import Q
from .models import *
# from django.db.models.functions import SHA2


class OrderForm(forms.Form):  # form for order page
    name = forms.CharField(label = "Name")
    lastname = forms.CharField(label = "Lastname",widget=forms.TextInput(attrs={'placeholder': 'lastname'}))
    user_address = forms.CharField(label = "Your address" ,max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    user_mobile = forms.CharField(label="Your mobile number", max_length=15)

    def clean_user_mobile(self):
        number = self.cleaned_data['user_mobile']
        if (len(number) < 10) or (len(number) >= 11):
            raise forms.ValidationError("This wrong number")
        return number

    def clean_user_address(self):
        value = self.cleaned_data['user_address']
        if (len(value) < 5):
            raise forms.ValidationError("Your address too short.")
        return value

class UserInfForm_(forms.Form):
    name = forms.CharField(label="Name", max_length=50)
    lastname = forms.CharField(label="Lastname", max_length=50)
    login = forms.CharField(label="Login", max_length=50)
    password_1 = forms.CharField(widget=forms.PasswordInput, label="Password",min_length=8, max_length = 320)
    password_2 = forms.CharField(widget=forms.PasswordInput, label="Repeat Password", min_length=8, max_length = 320)
    mobile = forms.CharField(label="mobile number", max_length=15)
    email = forms.EmailField(label="Email")

    def clean_user_mobile(self):
        number = self.cleaned_data['user_mobile']
        if (len(number) < 10) or (len(number) >= 11):
            raise forms.ValidationError("This wrong number")
        return number

class UserInfForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50)
    lastname = forms.CharField(label="Lastname", max_length=50)
    login = forms.CharField(label="Login", max_length=50)
    password_1 = forms.CharField(widget=forms.PasswordInput, label="Password",min_length=8, max_length = 320)
    password_2 = forms.CharField(widget=forms.PasswordInput, label="Repeat Password", min_length=8, max_length = 320)
    mobile = forms.CharField(label="mobile number", max_length=15)
    email = forms.EmailField(label="Email")

    def clean_login(self):
        log = self.cleaned_data['login']
        user = USER.objects.filter(user_login=log)
        if (user):
            raise forms.ValidationError("Sorry this login already taken")
        return log

    def clean_email(self):
        em = self.cleaned_data['email']
        user = USER.objects.filter(user_email=em)
        if (user):
            raise forms.ValidationError("Sorry this email already taken")
        return em

    def clean_user_mobile(self):
        number = self.cleaned_data['user_mobile']
        if (len(number) < 10) or (len(number) >= 11):
            raise forms.ValidationError("This wrong number")
        return number

    def clean_password_2(self):
        password = self.cleaned_data['password_1']
        repeat_pass = self.cleaned_data["password_2"]
        if (password != repeat_pass):
            raise forms.ValidationError("Passwords don't match")
        return password

class UserSignInForm(forms.Form):
    login = forms.CharField(label="Login", max_length=50)
    password = forms.CharField(label="Password", min_length = 8, max_length=224, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        user = USER.objects.get(user_login = cleaned_data.get('login'))

        if not user:
            self.add_error("login", "Sorry this user doesn't exist")
        if ( user.password != SHA2(cleaned_data.get('password'), 224)):
            self.add_error('password', "Wrong password")

    # def clean_login(self):
    #     login = self.cleaned_data['login']
    #     user = USER.objects.filter(user_login = login)
    #     if (user):
    #         return login
    #     raise forms.ValidationError("This login doesn't exist")
    #     return login
    #
    # def clean_password(self):
    #     passwd = self.cleaned_data['password']
    #     login = self.cleaned_data['login']
    #     user = USER.objects.filter(user_login = login)
    #     if (user.password ):
    #         pass

class NewComicsForm(forms.Form):
    title = forms.CharField(label="title", max_length=50)
    about = forms.CharField(label="About comics", max_length=1000,widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))
    date_public = forms.DateField(label="Date of publication")
    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=5, min_value=1.00000)
    amount = forms.IntegerField(label="Amount")
    publisher = forms.ModelChoiceField(label="Publisher",queryset=PUBLISHER.objects.all() )
    author = forms.ModelMultipleChoiceField(label="Author", queryset=AUTHOR.objects.all())
    comics_image = forms.ImageField()

    def clean_title(self):
        title = self.cleaned_data['title']
        comics = COMICS.objects.filter(comics_t__iexact=title)
        if (comics):
            raise forms.ValidationError("Sorry this comics already exist")
        return title

class EditComicsForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50)
    about = forms.CharField(label="About comics", max_length=1000,widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))
    date_public = forms.DateField(label="Date of publication")
    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=5, min_value=1.00000)
    amount = forms.IntegerField(label="Amount")



class NewPublisherForm(forms.Form):
    name = forms.CharField(label="Publisher name", max_length=50)
    about = forms.CharField(label="About publisher", max_length=1000, widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))

    def clean_name(self):
        name = self.cleaned_data['name']
        publish = PUBLISHER.objects.filter(publisher_name__iexact=name.capitalize())
        if (publish):
            raise forms.ValidationError("Sorry this publisher already exist")
        return name

class NewAuthorForm(forms.Form):
    name = forms.CharField(label="Author name", max_length=50)
    lastname = forms.CharField(label="Author lastname", max_length=50)
    birth = forms.DateField(label="Date of birth")
    about = forms.CharField(label="About this auhtor", max_length=1000, widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        lastname =cleaned_data.get('lastname')
        birth = cleaned_data.get("birth")

        auth = AUTHOR.objects.filter(Q(author_name__iexact = name.capitalize()), Q(author_lastname__iexact = lastname.capitalize()))
        if(auth):
            raise forms.ValidationError("This author already exists")


class EditAuthorForm(forms.Form):
    name = forms.CharField(label="Author name", max_length=50)
    lastname = forms.CharField(label="Author lastname", max_length=50)
    birth = forms.DateField(label="Date of birth")
    about = forms.CharField(label="About this auhtor", max_length=1000, widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))
# class RegistrForm(forms.Form):
#     name = forms.CharField(label="Your name", max_length=50)
#     lastname = forms.CharField(label="Your lastname", max_length=50)
#     login = forms.CharField(label="Login", max_length=50)
#     email = forms.EmailField(label="Email")
#     mobile = forms.CharField(label="mobile number", max_length=15)
#     password = forms.

class EditPublisherForm(forms.Form):
    name = forms.CharField(label="Publisher name", max_length=50)
    about = forms.CharField(label="About publisher", max_length=1000, widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))


class ManageOrderForm(forms.Form):
    status = forms.ModelChoiceField(label="Status",queryset=STATUS.objects.all() )
