from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Home, Address, Reserve, Comment, Rating, Search
from .forms import HomeForm, AddressForm, ReserveForm, CommentForm, RatingForm, SearchForm
from django.contrib.auth.decorators import login_required

def init_page(request):
    return render(request, 'airbnb/init_page.html')

def home_list(request):
    homes = Home.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    return render(request, 'airbnb/home_list.html', {'homes': homes})

def home_detail(request, pk):
    home = get_object_or_404(Home, pk=pk)
    rated = False
    reservation = False
    reserve_count = 0
    reserve = None
    
    if request.user.is_authenticated:    
        rate_count = Rating.objects.filter(
            home=pk,
            user=request.user
        ).count()

        if rate_count > 0:
            rated = True
        
        user_reserve = Reserve.objects.filter(
            home=pk,
            user=request.user
        )

        reserve_count = Reserve.objects.filter(
            home=pk,
            user=request.user
        ).count()

        if reserve_count > 0:
            reservation = True

        if reservation == True:
            reserve = get_object_or_404(user_reserve)

    return render(
        request, 
        'airbnb/home_detail.html', 
        {'home': home, 
        'rated': rated, 
        'reserve': reserve, 
        'reservation': reservation
        }
    )

@login_required
def home_new(request):
    if request.method == "POST":
        form = HomeForm(request.POST, request.FILES)
        if form.is_valid():
            home = form.save(commit=False)
            home.owner = request.user
            home.save()
            return redirect('home_address', pk=home.pk)
    else:
        form = HomeForm()
    return render(request, 'airbnb/home_edit.html', {'form': form})

@login_required
def home_address(request, pk):
    home = get_object_or_404(Home, pk=pk)

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.save()
            home.address = get_object_or_404(Address, pk=address.pk)
            home.save()
            return redirect('home_detail', pk=home.pk)
    else:
        form = AddressForm()
    return render(request, 'airbnb/home_address.html', {'form': form})

@login_required
def home_edit(request, pk):
    home = get_object_or_404(Home, pk=pk)

    if request.method == "POST":
        form = HomeForm(request.POST, request.FILES, instance=home)
        if form.is_valid():
            home = form.save(commit=False)
            home.owner = request.user
            home.save()
            return redirect('home_address', pk=home.pk)
    else:
        form = HomeForm(instance=home)
    return render(request, 'airbnb/home_edit.html', {'form': form})

def home_reservation(request, pk):
    home = get_object_or_404(Home, pk=pk)
    total_value = 0
    daily_cost = home.price

    if request.method == "POST":
        form = ReserveForm(request.POST)
        if form.is_valid():
            reserve = form.save(commit=False)

            is_reserved = Reserve.objects.filter(
                home=pk,
                user=request.user
            ).count()

            if is_reserved > 0:
                return redirect('home_detail', pk=home.pk)
            else:
                reserve.user = request.user
                reserve.home = home
                
                total_days = abs((reserve.final_date - reserve.initial_date).days)
            
                reserve.total_value = (daily_cost * total_days) * reserve.number_peoples
                reserve.save() 
                return redirect('home_detail', pk=home.pk)
    else:
        form = ReserveForm()
    return render(request, 'airbnb/home_reservation.html', {'form': form})

@login_required
def rating(request, pk):
    home = get_object_or_404(Home, pk=pk)
    rated = False

    if request.user.is_authenticated:    
        rate_count = Rating.objects.filter(
            home=pk,
            user=request.user
        ).count()

    if rate_count > 1:
        rated = True

    if rated:
        return redirect('home_detail', pk=home.pk)
    else:
        if request.POST.get('star') is None:
            return redirect('home_detail', pk=home.pk)
        else:
            rating = Rating.objects.create(user=request.user, home=home)
            rating.stars = request.POST.get('star')
            rating.save()
            return redirect('home_detail', pk=home.pk)

def search_list(request):
    home_searched = False

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.user = request.user
            search.save()
            
            homes = Home.objects.filter(address__city = search.local)

            homes_count = Home.objects.filter(address__city = search.local).count()

            if homes_count > 0:
                home_searched = True

            return render(
                request, 
                'airbnb/home_search.html', 
                {'homes': homes, 
                'search': search,
                'home_searched': home_searched}
            )
    else:
        form = SearchForm()
    return render(request, 'airbnb/init_page.html', {'form': form})

@login_required
def home_publish(request, pk):
    home = get_object_or_404(Home, pk=pk)
    home.publish()
    return redirect('home_detail', pk=pk)

def publish(self):
    self.published_date = timezone.now()
    self.save()

@login_required
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

