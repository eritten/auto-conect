from django.urls import reverse
from datetime import datetime, time
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_date
from .models import Order, User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.views.generic import ListView
from .forms import ServiceRequestForm
from .forms import ReviewForm
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Order, Review
from .forms import ProfileForm
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validate password strength (optional)
        if len(password1) < 8:
            messages.error(
                request, "Password must be at least 8 characters long.")
            return redirect('signup')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check for existing username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Check for existing email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(
            username=username, email=email, password=password1)
        user.save()

        messages.success(
            request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'registration/signup.html')


def mechanic_list_view(request):
    mechanics = Profile.objects.filter(user_type='me')
    return render(request, 'mechanic_list.html', {'mechanics': mechanics})


def home_view(request):
    mechanics = Profile.objects.filter(user_type='me')
    user_type = None
    driver_orders = None
    mechanic_orders = None

    if request.user.is_authenticated:
        user_type = request.user.profile.user_type
        if user_type == 'dr':
            driver_orders = Order.objects.filter(driver=request.user)
        elif user_type == 'me':
            mechanic_orders = Order.objects.filter(mechanic=request.user)

    context = {
        'mechanics': mechanics,
        'user_type': user_type,
        'driver_orders': driver_orders,
        'mechanic_orders': mechanic_orders,
    }
    return render(request, 'home.html', context)


@login_required
def complete_profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile,
                           user_type=request.user.profile.user_type)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_profile_complete = True
            profile.save()
            form.save_m2m()  # This saves the skills for mechanics
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile,
                           user_type=request.user.profile.user_type)

    return render(request, 'complete_profile.html', {'form': form})


@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})


@login_required
def order_mechanic_view(request, mechanic_id):
    mechanic = get_object_or_404(User, id=mechanic_id, profile__user_type='me')
    if request.method == 'POST':
        note = request.POST.get('note')
        location = request.POST.get('location')
        preferred_date_str = request.POST.get('preferred_date')

        if note and location and preferred_date_str:
            try:
                preferred_date = parse_date(preferred_date_str)
                if preferred_date:
                    preferred_datetime = datetime.combine(
                        preferred_date, time())
                    preferred_datetime = make_aware(preferred_datetime)
                else:
                    raise ValueError("Invalid date format")

                order = Order.objects.create(
                    driver=request.user,
                    mechanic=mechanic,
                    note=note,
                    location=location,
                    service_date=preferred_datetime
                )

                # Generate the order URL
                order_url = request.build_absolute_uri(
                    reverse('accept_order', args=[order.id]))

                # Send email
                send_mail(
                    'New Mechanic Order',
                    f'{request.user.username} has requested your service.\nLocation: {location}\nPreferred Date: {preferred_date_str}\nNote: {note}\n\nClick here to accept the order: {order_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [mechanic.email],
                )

                messages.success(
                    request, "Your service request has been sent successfully!")
                return redirect('home')
            except ValueError:
                messages.error(
                    request, "Invalid date format. Please use YYYY-MM-DD.")
        else:
            messages.error(
                request, "Please provide a note, location, and preferred date.")

    return render(request, 'order_mechanic.html', {'mechanic': mechanic})


@login_required
def review_mechanic_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.driver = request.user
            review.mechanic = order.mechanic
            review.save()
            order.status = 'completed'
            order.save()
            return redirect('home')
    else:
        form = ReviewForm()

    return render(request, 'review_mechanic.html', {'order': order, 'form': form})


@login_required
def service_request_view(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.driver = request.user
            service_request.save()
            messages.success(request, "Service request created successfully.")
            return redirect('home')
    else:
        form = ServiceRequestForm()

    return render(request, 'service_request.html', {'form': form})


class MechanicListView(ListView):
    model = Profile
    template_name = 'mechanic_list.html'
    context_object_name = 'mechanics'
    paginate_by = 9  # Number of mechanics per page

    def get_queryset(self):
        return Profile.objects.filter(user_type='me')


@login_required
def accept_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, mechanic=request.user)
    if request.method == 'POST':
        order.status = 'in_progress'
        order.save()
        messages.success(request, "You have accepted the order.")
        return redirect('home')
    return render(request, 'accept_order.html', {'order': order})
