from django.shortcuts import render

def accomodation_list(request):
    return render(request, 'airbnb/accomodation_list.html', {})
# Create your views here.
