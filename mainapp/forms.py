from django import forms

class FindDestinationForm(forms.Form):
    place = forms.CharField(label='', widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super(FindDestinationForm, self).__init__(*args, **kwargs)
        self.fields['place'].widget.attrs.update({'class' : 'col-sm-10 col-form-label', 'placeholder': 'Where ?'})