from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.views.decorators.csrf import csrf_exempt
from .models import Home, Address, Reserve, Comment, Rating, Search
from .forms import HomeForm, AddressForm, ReserveForm, CommentForm, RatingForm, SearchForm
from .serializers import HomeSerializer, UserSerializer, PostSerializer
from users.models import CustomUser
from blog.models import Post

import logging

logger = logging.getLogger(__name__)

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

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

            if home.image == '../static/img/img_notfound.png':
                logger.warning('Imagem da acomodação não foi anexada.')

            return redirect('home_address', pk=home.pk)
        else:
            messages.error(request, 'Erro! Verifique se os dados estão corretos.')
            logger.error('Erro! Tentativa em submeter dados inválidos')
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
            messages.success(request, 'Dados salvos com sucesso!')
            logger.info('Dados salvos corretamente')

            return redirect('home_detail', pk=home.pk)
        else:
            messages.error(request, 'Erro! Verifique se os dados estão corretos.')
            logger.error('Erro! Tentativa em submeter dados inválidos')

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
            messages.error(request, 'Erro! Verifique se os dados estão corretos.')
            logger.error('Ausência de dados em um ou mais campos do formulário. Acomodação não editada')
    else:
        form = HomeForm(instance=home)
    return render(request, 'airbnb/home_edit.html', {'form': form})

def home_reservation(request, pk):
    home = get_object_or_404(Home, pk=pk)

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
                logger.warning('Não foi possível reservar. Acomodação já está reservada por este usuário.')
                messages.error(request, 'Erro, você ja reservou esta acomodação.')
            else:
                reserve.user = request.user
                reserve.home = home
                reserve.set_total_value()

                reserve.save() 
                messages.success(request, 'Reserva feita com sucesso!')
                return redirect('home_detail', pk=home.pk)
        else:
            messages.error(request, 'Erro! Verifique se os dados estão corretos.')
            logger.error('Ausência de dados em um ou mais campos do formulário. Reserva não realizada')
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
            messages.success(request, 'Acomodação avaliada com sucesso.')
            return redirect('home_detail', pk=home.pk)

@login_required
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

            logger.info('Busca realizada na cidade de : ' + search.local)

            if homes_count > 0:
                home_searched = True
                messages.success(request, 'Veja as acomodações que encontramos para você.')
                logger.info('Acomodações encontradas no local de busca.')
            else:
                messages.warning(request, 'Não foi possível encontrar acomodações nesse local.')
                logger.warning('Localização sem acomodações encontradas na base de dados.')

            return render(
                request, 
                'airbnb/home_search.html', 
                {'homes': homes, 
                'search': search,
                'home_searched': home_searched}
            )
        else:
            logger.error('Ausência de dados em um ou mais campos do formulário. Pesquisa não realizada')
            messages.warning(request, 'Atenção, preencha todos os campos para realizar a pesquisa!')
    else:
        form = SearchForm()
    return render(request, 'airbnb/init_page.html', {'form': form})

@login_required
def home_publish(request, pk):
    home = get_object_or_404(Home, pk=pk)
    home.publish()
    messages.success(request, 'Publicação feita com sucesso!')
    return redirect('home_detail', pk=pk)

def publish(self):
    self.published_date = timezone.now()
    self.save()

@login_required
def home_remove(request, pk):
    home = get_object_or_404(Home, pk=pk)
    home.delete()
    messages.warning(request, 'Acomodação removida com sucesso!')
    return redirect('home_list')

def add_comment_to_home(request, pk):
    home = get_object_or_404(Home, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.home = home
            comment.save()
            messages.success(request, 'Comentário adicionado com sucesso.')
            return redirect('home_detail', pk=home.pk)
        else:
            messages.error(request, 'Erro! Verifique se os dados estão corretos.')
    else:
        form = CommentForm()
    return render(request, 'airbnb/add_comment_to_home.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    messages.success(request, 'Comentário publicado com sucesso!')
    return redirect('home_detail', pk=comment.home.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    messages.warning(request, 'Comentário removido com sucesso!')
    logger.warning('Um comentário foi removido do banco de dados.')
    return redirect('home_detail', pk=comment.home.pk)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated|ReadOnly])
def rest_home_list(request):
    if request.method == 'GET':
        homes = Home.objects.filter().order_by('-created_date')
        serializer = HomeSerializer(homes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = HomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated|ReadOnly])
def rest_home_detail(request, pk):
    try:
        home = Home.objects.get(pk=pk)
    except Home.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HomeSerializer(home)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = HomeSerializer(home, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        home.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated|ReadOnly])
def rest_user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.filter()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated|ReadOnly])
def rest_user_detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated|ReadOnly])
def rest_post_list(request):
    if request.method == 'GET':
        posts = Post.objects.filter().order_by('-created_date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated|ReadOnly])
def rest_post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)