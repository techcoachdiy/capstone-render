from django.urls import path
from . import views
from .views import LoginView, LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),   
    path("topics/new/", views.topic_entry, name="topic_entry"), 
    path("topics/<slug:topic_slug>/", views.topic_page, name="topic_page"),
    path("topics/<slug:topic_slug>/entries/new/", views.create_entry, name="create_entry"),
    path("topics/<slug:topic_slug>/entries/<slug:entry_slug>/", views.entry_detail, name="entry_detail"),
    path("topics/<slug:topic_slug>/entries/<slug:entry_slug>/edit/", views.submit_edit, name="submit_edit"),
    path("dashboard/review/", views.review_dashboard, name="review_dashboard"),
    path("dashboard/review/<int:revision_id>/", views.review_revision, name="review_revision"),
    #path("entries/<slug:entry_slug>/edit/", views.revision_create, name="revision_create"),
    path("foodcomponents/add/", views.bulk_foodcomponent_entry, name="bulk_foodcomponent_entry"),
    path("recipes/new/", views.recipe_entry, name='recipe_entry'),
    path("recipes/<int:recipe_id>/edit/", views.edit_recipe, name='editrecipe'),
]