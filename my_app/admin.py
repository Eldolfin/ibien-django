from django.contrib import admin
from .models import Sell, UserProfile

# This allows the admins to see the data in the admin panel
# as well as edit/delete it
admin.site.register(Sell)
admin.site.register(UserProfile)
