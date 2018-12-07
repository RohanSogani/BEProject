from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SiteRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def save(self,commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password1']

        if commit:
            user.save()

        return user



#defines form to upload apk
class apkUploadForm(forms.Form):
	docfile = forms.FileField(label='Select file')
