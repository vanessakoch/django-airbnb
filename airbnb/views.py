from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Home, Comment
from .forms import HomeForm, CommentForm
from django.contrib.auth.decorators import login_required

def home_list(request):
    homes = Home.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    return render(request, 'airbnb/home_list.html', {'homes': homes})

def home_detail(request, pk):
    home = get_object_or_404(Home, pk=pk)
    return render(request, 'airbnb/home_detail.html', {'home': home})

@login_required
def home_new(request):
    if request.method == "POST":
        form = HomeForm(request.POST, request.FILES)
        if form.is_valid():
            home = form.save(commit=False)
            home.owner = request.user
            home.save()
            return redirect('home_detail', pk=home.pk)
    else:
        form = HomeForm()
    return render(request, 'airbnb/home_edit.html', {'form': form})

def home_edit(request, pk):
    home = get_object_or_404(Home, pk=pk)
    if request.method == "POST":
        form = HomeForm(request.POST, request.FILES, instance=home)
        if form.is_valid():
            home = form.save(commit=False)
            home.owner = request.user
            home.save()
            return redirect('home_detail', pk=home.pk)
    else:
        form = HomeForm(instance=home)
    return render(request, 'airbnb/home_edit.html', {'form': form})

def home_publish(request, pk):
    home = get_object_or_404(Home, pk=pk)
    home.publish()
    return redirect('home_detail', pk=pk)

def publish(self):
    self.published_date = timezone.now()
    self.save()

def home_remove(request, pk):
    home = get_object_or_404(Home, pk=pk)
    home.delete()
    return redirect('home_list')

def add_comment_to_home(request, pk):
    home = get_object_or_404(Home, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.home = home
            comment.save()
            return redirect('home_detail', pk=home.pk)
    else:
        form = CommentForm()
    return render(request, 'airbnb/add_comment_to_home.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('home_detail', pk=comment.home.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('home_detail', pk=comment.home.pk)