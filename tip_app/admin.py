from django.contrib import admin
from .models import User, Tip

# Register the User model with default admin settings
admin.site.register(User)

# Register the Tip model with basic configuration
@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'total_amount', 'tip_amount', 'created_at')

