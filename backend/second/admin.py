from django.contrib import admin
from second.models import *


# class CalculatorAdmin(admin.ModelAdmin):
#     list_display = ('a', 'b', 'c', 'root1', 'root2')


admin.site.register(Calculator)

