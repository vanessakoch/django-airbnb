from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Home
from .forms import HomeForm

def home_list(request):
    homes = Home.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    return render(request, 'airbnb/home_list.html', {'homes': homes})

def home_detail(request, pk):
    home = get_object_or_404(Home, pk=pk)
    home.save()
    return render(request, 'airbnb/home_detail.html')

def home_new(request):
    if request.method == "POST":
        form = HomeForm(request.POST)
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
        form = HomeForm(request.POST, instance=post)
        if form.is_valid():
            home = form.save(commit=False)
            home.owner = request.user
            home.save()
            return redirect('home_detail', pk=post.pk)
    else:
        form = HomeForm(instance=home)
    return render(request, 'airbnb/home_edit.html', {'form': form})