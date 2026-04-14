from django.contrib import admin

# Register your models here.
from .models import Topic, FoodComponent, Entry, Revision, Recipe 

admin.site.register(Topic)
admin.site.register(FoodComponent)
admin.site.register(Entry)
admin.site.register(Revision)
admin.site.register(Recipe)
