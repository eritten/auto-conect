from .models import Review
from .models import Order
from .models import ServiceRequest
from .models import Profile, Skill
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='First name')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Last name')
    email = forms.EmailField(
        max_length=254, help_text='Required. Provide a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['profile_image', 'city', 'lat', 'long', 'bio',
                  'user_type', 'hourly_rate', 'telephone_number', 'skills']

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user_type == 'dr':
            self.fields.pop('hourly_rate')
            self.fields.pop('skills')
        self.fields['user_type'].widget.attrs.update(
            {'onchange': 'showHideHourlyRateAndSkills()'})


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['description', 'location']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['note', 'location', 'service_date']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
