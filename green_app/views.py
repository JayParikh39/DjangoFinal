from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model

from .models import (
    GreenIdea, Category, UserProfile, Comment, Rating, 
    Project, Event, Resource, Collaboration, Newsletter
)
from .forms import (
    CustomUserCreationForm, GreenIdeaForm, UserProfileForm, 
    CommentForm, RatingForm, ProjectForm, EventForm, 
    ResourceForm, CollaborationForm, NewsletterForm, CategoryForm
)
from .utils import update_user_visit_session
from datetime import datetime

# 1. Index View (Enhanced)
class IndexView(ListView):
    model = GreenIdea
    template_name = 'green_app/index.html'
    context_object_name = 'ideas'
    ordering = ['-submission_date']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context.update(update_user_visit_session(self.request))
        context['categories'] = Category.objects.all()
        context['featured_ideas'] = GreenIdea.objects.filter(is_featured=True)[:6]
        context['recent_events'] = Event.objects.filter(date__gte=now()).order_by('date')[:3]
        context['top_resources'] = Resource.objects.order_by('-download_count')[:5]
        return context

# 2. Idea Detail View (Enhanced)
class IdeaDetailView(DetailView):
    model = GreenIdea
    template_name = 'green_app/idea_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idea = self.get_object()
        idea.views_count += 1
        idea.save()
        
        context['comments'] = idea.comments.filter(is_approved=True).order_by('-created_at')
        context['comment_form'] = CommentForm()
        context['rating_form'] = RatingForm()
        context['average_rating'] = idea.ratings.aggregate(Avg('rating'))['rating__avg']
        context['total_ratings'] = idea.ratings.count()
        context['related_projects'] = idea.projects.all()[:3]
        return context

# 3. User Profile View
@login_required
def user_profile_view(request, username=None):
    if username:
        user = get_object_or_404(get_user_model(), username=username)
    else:
        user = request.user
    
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST' and request.user == user:
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile', username=user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'form': form,
        'user_ideas': user.greenidea_set.all().order_by('-submission_date')[:5],
        'user_projects': user.project_set.all().order_by('-created_at')[:5],
    }
    return render(request, 'green_app/user_profile.html', context)

# 4. Comment Management View
@login_required
def add_comment_view(request, idea_id):
    idea = get_object_or_404(GreenIdea, id=idea_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.idea = idea
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    return redirect('idea_detail', pk=idea_id)

# 5. Rating Management View
@login_required
def add_rating_view(request, idea_id):
    idea = get_object_or_404(GreenIdea, id=idea_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(
                idea=idea, 
                user=request.user,
                defaults={'rating': form.cleaned_data['rating']}
            )
            if not created:
                rating.rating = form.cleaned_data['rating']
                rating.save()
            messages.success(request, 'Rating submitted successfully!')
        else:
            messages.error(request, 'Error submitting rating.')
    return redirect('idea_detail', pk=idea_id)

# 6. Project Management Views
class ProjectListView(ListView):
    model = Project
    template_name = 'green_app/project_list.html'
    context_object_name = 'projects'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'green_app/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collaborations'] = self.object.collaborations.all()
        context['collaboration_form'] = CollaborationForm()
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'green_app/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)

# 7. Event Management Views
class EventListView(ListView):
    model = Event
    template_name = 'green_app/event_list.html'
    context_object_name = 'events'
    ordering = ['date']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        upcoming = self.request.GET.get('upcoming')
        if upcoming == 'true':
            queryset = queryset.filter(date__gte=now())
        return queryset

class EventDetailView(DetailView):
    model = Event
    template_name = 'green_app/event_detail.html'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'green_app/event_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

# 8. Resource Management Views
class ResourceListView(ListView):
    model = Resource
    template_name = 'green_app/resource_list.html'
    context_object_name = 'resources'
    ordering = ['-created_at']
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        return queryset

class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'green_app/resource_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.get_object()
        resource.download_count += 1
        resource.save()
        return context

class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'green_app/resource_form.html'
    success_url = reverse_lazy('resource_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'Resource uploaded successfully!')
        return super().form_valid(form)

# 9. Collaboration Management View
@login_required
def collaboration_request_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = CollaborationForm(request.POST)
        if form.is_valid():
            collaboration = form.save(commit=False)
            collaboration.project = project
            collaboration.collaborator = request.user
            collaboration.save()
            messages.success(request, 'Collaboration request sent successfully!')
        else:
            messages.error(request, 'Error sending collaboration request.')
    return redirect('project_detail', pk=project_id)

@login_required
def collaboration_response_view(request, collaboration_id, response):
    collaboration = get_object_or_404(Collaboration, id=collaboration_id)
    if request.user == collaboration.project.creator:
        if response in ['accepted', 'rejected']:
            collaboration.status = response
            collaboration.save()
            messages.success(request, f'Collaboration request {response}!')
    return redirect('project_detail', pk=collaboration.project.id)

# 10. Newsletter Management Views
class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'green_app/newsletter_list.html'
    context_object_name = 'newsletters'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        # Staff users can see all newsletters, regular users only see published ones
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(is_published=True)

class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'green_app/newsletter_detail.html'

class NewsletterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'green_app/newsletter_form.html'
    success_url = reverse_lazy('newsletter_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Automatically publish newsletters created by staff
        form.instance.is_published = True
        form.instance.published_at = now()
        messages.success(self.request, 'Newsletter created and published successfully!')
        return super().form_valid(form)

# Existing views (keeping for compatibility)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'green_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'green_app/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('index')

class SubmitIdeaView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = GreenIdeaForm()
        return render(request, 'green_app/submit_idea.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = GreenIdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.submitted_by = request.user
            idea.save()
            return redirect('idea_detail', pk=idea.pk)
        return render(request, 'green_app/submit_idea.html', {'form': form})

def search_view(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    results = GreenIdea.objects.all().order_by('-submission_date')

    if query:
        results = results.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if category_id:
        results = results.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'green_app/search_results.html', {
        'results': results,
        'query': query or "all",
        'categories': categories
    })

def about_us_view(request):
    return render(request, 'green_app/about_us.html')

@login_required
def unregister_view(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('index')
    return render(request, 'green_app/unregister_confirm.html')

@login_required
def delete_idea_view(request, pk):
    idea = get_object_or_404(GreenIdea, pk=pk)
    if request.user == idea.submitted_by or request.user.is_superuser:
        if request.method == 'POST':
            idea.delete()
            return redirect('index')
        return render(request, 'green_app/delete_idea_confirm.html', {'idea': idea})
    return HttpResponseForbidden("You are not allowed to delete this idea.")

@login_required
def user_history_view(request):
    num_visits = request.session.get('num_visits', 0)
    last_visit = request.session.get('last_visit', 'First visit this session')

    if isinstance(last_visit, str) and last_visit != 'First visit this session':
        try:
            last_visit = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            last_visit = None

    request.session['num_visits'] = num_visits + 1
    request.session['last_visit'] = now().strftime('%Y-%m-%d %H:%M:%S')

    context = {
        'num_visits': num_visits + 1,
        'last_visit': last_visit
    }
    return render(request, 'green_app/user_history.html', context)

# Newsletter publication toggle for staff
@login_required
def toggle_newsletter_publication(request, newsletter_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to perform this action.")
    
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    newsletter.is_published = not newsletter.is_published
    
    if newsletter.is_published:
        newsletter.published_at = now()
        messages.success(request, f'Newsletter "{newsletter.title}" has been published.')
    else:
        newsletter.published_at = None
        messages.success(request, f'Newsletter "{newsletter.title}" has been unpublished.')
    
    newsletter.save()
    return redirect('newsletter_list')
