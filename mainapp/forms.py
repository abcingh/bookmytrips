from django import forms
from .models import Profile
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'dob', 'gender','description', 'avatar')
        widgets = {
            'dob': DateInput(),
            'description': forms.Textarea(attrs={'placeholder': 'Write some thing about you'})
        }


class FindDestinationForm(forms.Form):
    place = forms.CharField(label='', widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super(FindDestinationForm, self).__init__(*args, **kwargs)
        self.fields['place'].widget.attrs.update({'class' : 'col-sm-10 col-form-label', 'placeholder': 'Where ?'})
