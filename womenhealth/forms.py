from django import forms
from .models import Topic, Entry, FoodComponent, Recipe

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
        labels = {
            'name': 'New Topic Name'
        }
       #widgets = {
       #     'name': forms.TextInput(attrs={
       #         'placeholder': 'Enter new topic name ',
       #         'class': 'topic-input'}),
       # }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content', 'food_components']
        labels = {
            'title': 'Title',
            'content': 'Content',
            'food_components': 'Food Components',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'id': 'id_content',
                'rows':20, 
                'placeholder': 'Write a new article here ... ',
                'class': 'content-box'
            }),
            'food_components' : forms.SelectMultiple(attrs={
                'class': 'foodcomponent-select'
            }),
        }
    def clean_food_components(self):
        food_components = self.cleaned_data.get("food_components")
        if len(food_components) < 3 or len(food_components) > 5:
            raise forms.ValidationError(
                "Please enter between 3 and 5 food components."
            )
        return food_components
        
class BulkFoodComponentForm(forms.Form):
    names = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Enter one component per line"}),
        help_text="Enter one food component per line.",
        label="Food Components"
    )
    is_approved = forms.BooleanField(
        initial=True,
        required=False,
        label="Approve Immediately"
    )

    def clean_names(self):
        # nofmrlize input and return a list of unique names
        names_text = self.cleaned_data["names"]

        processed = []
        for line in names_text.splitlines():
            name = line.strip()
            if name and name.lower() not in [n.lower() for n in processed]:
                processed.append(name)
        if not processed:
            raise forms.ValidationError("Please enter at least one component.")
        
        return processed

# below is temporary .. need further check 
#class RevisionForm(forms.ModelForm):
#    suggested_ingredient = forms.CharField(
#        required=False,
#        help_text="Optional: suggest a new ingredient"
#    )

#    class Meta:
#        model = Revision
#        fields = ["content", "ingredients"]
#
#    ingredients = forms.ModelMultipleChoiceField(
#        queryset=Ingredient.objects.filter(is_approved=True),
#        widget=forms.CheckboxSelectMultiple,
#        required=True
#    )

#    def clean_ingredients(self):
#        ingredients = self.cleaned_data["ingredients"]
#        if not 3 <= len(ingredients) <= 5:
#            raise forms.ValidationError("Select between 3 and 5 ingredients.")
#        return ingredients

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'food_component', 'description', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe title'}),
            'food_component': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write recipe instructions..'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional image URL'}),
        }
        
