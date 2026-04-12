from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView as DjangoLoginView, 
    LogoutView as DjangoLogoutView,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.http import HttpResponse
from .models import Topic, Entry, Revision, FoodComponent, Recipe
from .forms import TopicForm, EntryForm, RecipeForm, BulkFoodComponentForm
from django.views.decorators.http import require_POST
import markdown

# Create your views here.
class LoginView(DjangoLoginView):
    template_name = "womenhealth/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("index")
    
class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("login")

User = get_user_model()

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "womenhealth/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "womenhealth/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "womenhealth/register.html")

#list all topics & recipes
def index(request):
    topics = Topic.objects.all()
    recipes = Recipe.objects.all().order_by('-created_at')

    return render(request, "womenhealth/index.html", {
        "topics": topics,
        "recipes": recipes
    })

def topic_page(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    entries = topic.entries.all()
    main_entry = entries.first()
    if main_entry: 
        main_entry_html = markdown.markdown(main_entry.content, extensions=['fenced_code', 'tables'])
    else:
        main_entry_html = None
        
    return render(request, "womenhealth/entry_detail.html", {
        "topic": topic, 
        "entries": entries,
        "entry": main_entry,
        "entry_html": main_entry_html
    })

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def topic_entry(request):
    if request.method == "POST":
        entered_topic = TopicForm(request.POST)
        if entered_topic.is_valid():
            entered_topic.save()
            return redirect("index")
    else:
        entered_topic = TopicForm()

    return render(request, "womenhealth/topic_entry.html", {
        "entered_topic": entered_topic 
    })

def entry_detail(request, topic_slug, entry_slug):
    entry = get_object_or_404(Entry, topic__slug=topic_slug, slug=entry_slug)
    entries_in_topic = entry.topic.entries.all()
    
    entry_html = markdown.markdown(entry.content, extensions=['fenced_code', 'tables'])

    recipes = Recipe.objects.filter(
        food_component__name__in=entry.food_components.values_list('name', flat=True))

    #print("Entry ID:", entry.id)
    #print("Entry title:", entry.title)
    #print("Recipes for this entry:", list(recipes))

    return render(request, "womenhealth/entry_detail.html", {
        "topic": entry.topic,
        "entry": entry,
        "entries": entries_in_topic,
        "entry_html": entry_html,
        "recipes": recipes
    })

@login_required
def create_entry(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)

    if request.method == "POST":
        form = EntryForm(request.POST)
        
        if form.is_valid():
            entry = form.save(commit=False)
            entry.topic = topic
            entry.created_by = request.user

            if request.user.is_staff:
                #entry.content = form.cleaned_data["content"]
                entry.save()
                form.save_m2m()
            else:
                entry.content = ""
                entry.status = "pending"
                entry.save()
                Revision.objects.create(
                    entry=entry,
                    content=form.cleaned_data["content"],
                    editor=request.user
                )
                #revision.foodcomponents.set(form.cleaned_data["foodcomponents"])
            return redirect("entry_detail", topic_slug=topic.slug, entry_slug=entry.slug)
    else:
        form = EntryForm()
        
    return render(request, "womenhealth/entry_form.html", {
        "topic": topic,
        "form": form,
        "form_title": "Create New Article"
    })

@login_required
def submit_edit(request, topic_slug, entry_slug):
    entry = get_object_or_404(Entry, topic__slug=topic_slug, slug=entry_slug)

    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)

        if form.is_valid():
            content = form.cleaned_data["content"]
            entry.food_components.set(form.cleaned_data["food_components"])
            if request.user.is_staff:
                entry = form.save()

            else:
                if content:
                    Revision.objects.create(
                        entry=entry,
                        content=request.POST["content"],
                        editor=request.user,
                        status="pending"
                    )
        return redirect("entry_detail", topic_slug=entry.topic.slug, entry_slug=entry.slug)
    else:
        form = EntryForm(instance=entry)
    
    return render(request, "womenhealth/entry_form.html", {
        "entry": entry,
        "form": form,  
        "topic": entry.topic,
        "form_title": "Edit Article",  
    })

@user_passes_test(is_staff)
def review_dashboard(request):
    
    pending_revisions = Revision.objects.filter(status="pending") \
    .select_related("entry", "editor") \
    .order_by("-created_at")

    return render(request, "womenhealth/review_dashboard.html", {
        "pending_revisions": pending_revisions
    })

#def create_notification(user, message):
#    Notification.objects.create(
#        user=user,
#        message=message
#    )


@user_passes_test(is_staff)
@require_POST
def review_revision(request, revision_id):
    revision = get_object_or_404(Revision, id=revision_id)

    if revision.status != "pending":
        return redirect("review_dashboard")
        
    action = request.POST.get("action")

    if action == "approve":
        revision.status = "approved"
        revision.save()

        article = revision.entry
        article.content = revision.content
        article.save()

        revision.save()
#        create_notification(
#        entry.author,
#        f"Your article "{entry.title}" was approved."
#       )

    elif action == "reject":
        revision.status = "rejected"
        revision.save()

#            create_notification(
#                entry.author,
#                f"Your article "{entry.title}" was rejected."
#            )
    return redirect("review_dashboard")

@login_required
@user_passes_test(is_staff)
def bulk_foodcomponent_entry(request):
    if request.method == "POST":
        form = BulkFoodComponentForm(request.POST)

        if form.is_valid():
            names = form.cleaned_data["names"]
            for name in names:
                FoodComponent.objects.get_or_create(
                    name=name,
                    defaults={
                        "is_approved": form.cleaned_data['is_approved'],
                        "created_by": request.user
                    }
                )
            return redirect("index")
    else:
        form = BulkFoodComponentForm()

    return render(request, "womenhealth/bulkfoodcomponent_form.html", {
        "form": form 
    })

@login_required
def recipe_entry(request):
    if request.method == "POST":
        entered_recipe = RecipeForm(request.POST)
        if entered_recipe.is_valid():
            recipe = entered_recipe.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect("index")
    else:
        entered_recipe = RecipeForm()

    return render(request, "womenhealth/recipe_form.html", {
        "form": entered_recipe,
        "title": "Add Recipe",
        "button_text": "Create"
    })

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if recipe.user != request.user:
        return redirect("index")
        
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, "womenhealth/recipe_form.html", {
        "form": form,
        "title": f"Edit Recipe: {recipe.title}",
        "button_text": "Save Changes"
    })