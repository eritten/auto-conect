from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from mapbox_location_field.forms import LocationField
from .models import Profile, Skill, ServiceRequest, Order, Review, Vehicle, Service, Availability


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
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.none(), required=False)

    class Meta:
        model = ServiceRequest
        fields = ['description', 'location', 'vehicle']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ServiceRequestForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(
                owner=user)


class OrderForm(forms.ModelForm):
    location = LocationField(map_attrs={"center": [
                             30, 30], "marker_color": "green", "placeholder": "Order location"})
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.none(), required=False)

    class Meta:
        model = Order
        fields = ['note', 'location', 'service_date', 'services', 'vehicle']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(
                owner=user)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'vin']


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time']
