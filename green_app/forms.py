from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    GreenIdea, UserProfile, Comment, Rating, Project, 
    Event, Resource, Collaboration, Newsletter, Category
)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

class GreenIdeaForm(forms.ModelForm):
    class Meta:
        model = GreenIdea
        fields = ['title', 'description', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'website', 'location', 'expertise_areas']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'website': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)]),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'idea', 'status', 'start_date', 'end_date', 'budget']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'budget': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'date', 'location', 'max_participants', 'is_online', 'registration_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'max_participants': forms.NumberInput(attrs={'min': '1'}),
            'registration_url': forms.URLInput(attrs={'placeholder': 'https://example.com/register'}),
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'resource_type', 'url', 'category', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'url': forms.URLInput(attrs={'placeholder': 'https://example.com/resource'}),
        }

class CollaborationForm(forms.ModelForm):
    class Meta:
        model = Collaboration
        fields = ['project', 'role', 'message']
        widgets = {
            'role': forms.TextInput(attrs={'placeholder': 'e.g., Developer, Designer, Researcher'}),
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your interest in collaborating...'}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }