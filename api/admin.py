from django.contrib import admin
from .models import Profile, Review, Order


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'city',
                    'telephone_number', 'hourly_rate')
    list_filter = ('user_type', 'city')
    search_fields = ('user__username', 'user__email', 'city')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'profile_image', 'telephone_number')
        }),
        ('Location', {
            'fields': ('city', 'lat', 'long')
        }),
        ('Profile Details', {
            'fields': ('bio', 'user_type', 'hourly_rate', 'mechanic_skills')
        }),
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('driver', 'mechanic', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('driver__username', 'mechanic__username', 'content')
    fieldsets = (
        ('Review Details', {
            'fields': ('driver', 'mechanic', 'content', 'rating', 'created_at')
        }),
    )
    readonly_fields = ('created_at',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('driver', 'mechanic', 'ordered_at', 'status')
    list_filter = ('status', 'ordered_at')
    search_fields = ('driver__username', 'mechanic__username', 'location')
    fieldsets = (
        ('Order Information', {
            'fields': ('driver', 'mechanic', 'note', 'location')
        }),
        ('Status and Timing', {
            'fields': ('ordered_at', 'status')
        }),
    )
    readonly_fields = ('ordered_at',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)

admin.site.site_title = "Karim Project Dashboard"
admin.site.site_header = "Karim Project Admin Dashboard"
admin.site.site_index = "Welcome to Karim Project Dashboard"
