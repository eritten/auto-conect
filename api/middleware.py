from django.shortcuts import redirect
from django.urls import reverse
from .models import Profile


class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if the profile exists, create one if it doesn't
            profile, created = Profile.objects.get_or_create(user=request.user)

            # Redirect to complete profile if not complete
            if not profile.is_profile_complete and request.path not in [reverse('complete_profile'), reverse('logout')]:
                return redirect('complete_profile')

        response = self.get_response(request)
        return response
