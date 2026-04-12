from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

class User(AbstractUser):
    pass

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class FoodComponent(models.Model):
    name = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        super().save(*args, **kwargs)
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='unique_lower_foodcomponent'
            )
        ]
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Entry(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="entries"
        #check related_name is necessary
    )
    content = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="entries_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    food_components = models.ManyToManyField(FoodComponent, blank=True, related_name="entries")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Entry.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Revision(models.Model):
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name="revisions",
    )
    #topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField()
    editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    STATUS_CHOICE=[
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected")
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICE,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        permissions = [
            ("can_review_entry", "Can review and approve entries"),
        ]

    def __str__(self):
        return f"{self.entry.title} ({self.status})"


class Recipe(models.Model):
    title = models.CharField(max_length=64)
    food_component = models.ForeignKey(
        FoodComponent,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    #entry = models.ForeignKey(
    #    Entry,
    #    on_delete=models.CASCADE,
    #    related_name="recipes"
    #)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} = {self.food_component} ({self.title})"