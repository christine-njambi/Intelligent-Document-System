
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ClassModel, StudentModel, TransactionModel, UploadedImage

from django import forms

from django.forms.widgets import PasswordInput, TextInput


# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):
    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

# - Create Class

class CreateClassForm(forms.ModelForm):
    class Meta:
        model = ClassModel
        fields = ['name', 'class_motto'] 

# - Create a Student 

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        fields = ['name', 'age', 'class_attending']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionModel
        fields = ['amount', 'student_number']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']

# - Authenticate a user (Model Form)

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
