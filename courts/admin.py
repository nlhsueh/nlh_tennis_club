from django.contrib import admin
from .models import Court

class CourtAdmin(admin.ModelAdmin):
  list_display = ("city", "courtname", "courttype", "photo")

admin.site.register(Court, CourtAdmin)

