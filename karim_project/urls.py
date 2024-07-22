from django.contrib import admin
from django.urls import path, include
from api.views import (
    signup_view,
    home_view,
    profile_view,
    complete_profile_view,
    order_mechanic_view,
    review_mechanic_view,
    mechanic_list_view,
    service_request_view,
    MechanicListView,
    accept_order_view,
    add_vehicle_view,
    set_availability_view
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup_view, name="signup"),
    path('', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('complete-profile/', complete_profile_view, name='complete_profile'),
    path('order-mechanic/<int:mechanic_id>/',
         order_mechanic_view, name='order_mechanic'),
    path('review-mechanic/<int:order_id>/',
         review_mechanic_view, name='review_mechanic'),
    path('mechanics/', mechanic_list_view, name='mechanic_list'),
    path('service-request/', service_request_view, name='service_request'),
    path('mechanics-list/', MechanicListView.as_view(), name='mechanics_list'),
    path('accept-order/<int:order_id>/', accept_order_view, name='accept_order'),
    path('add-vehicle/', add_vehicle_view, name='add_vehicle'),
    path('set-availability/', set_availability_view, name='set_availability'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
