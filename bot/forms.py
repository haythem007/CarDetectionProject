from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import  UserChangeForm, UserCreationForm

SUBJECT_CHOICES = (
    ('-----', '-----'),
    ('info', 'Request more information'),
    ('contribute', 'Learn more about how to contribute'),
    ('bug', 'Correction or bug report'),
    ('other', 'Other (please specify)')
)

class UserForm(forms.ModelForm):
     password = forms.CharField(widget=forms.PasswordInput)
     class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EditProfileForm(UserChangeForm):
        template_name='edit_profile'
        class Meta:
                model = User
                fields = ['username', 'email', 'password', 'last_name', 'first_name']
                       
                        
                        

                


class ContactUsForm(forms.Form):
    name = forms.CharField(required=True, max_length=512)
    email = forms.EmailField(required=True)

    subject = forms.ChoiceField(
        required=True, choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': "form-control"}))

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': "form-control"}),
        required=True)

    decoy = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super(ContactUsForm, self).clean()

        if cleaned_data['subject'] == '-----':
            self._errors["subject"] = self.error_class([
                "Please specify a subject"])

        if 'decoy' in cleaned_data and len(cleaned_data['decoy']) > 0:
            self._errors["decoy"] = self.error_class([
                "Please leave this field blank"])

        return cleaned_data      

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)              


