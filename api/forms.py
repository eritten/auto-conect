from .models import Review
from .models import Order
from .models import ServiceRequest
from .models import Profile, Skill
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from mapbox_location_field.forms import LocationField


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
    location = LocationField(map_attrs={"center": [
                             30, 30], "marker_color": "red", "placeholder": "Select your location"})

    class Meta:
        model = Profile
        fields = ['profile_image', 'city', 'location', 'bio',
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
    location = LocationField(map_attrs={"center": [
                             30, 30], "marker_color": "blue", "placeholder": "Service location"})

    class Meta:
        model = ServiceRequest
        fields = ['description', 'location']


class OrderForm(forms.ModelForm):
    location = LocationField(map_attrs={"center": [
                             30, 30], "marker_color": "green", "placeholder": "Order location"})

    class Meta:
        model = Order
        fields = ['note', 'location', 'service_date']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
