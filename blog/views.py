from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Post, PostComment, PostLike, PostDislike
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    liked = False
    disliked = False
    percent_likes = 0
    percent_dislikes = 0

    if request.user.is_authenticated:
        
        likes_count = PostLike.objects.filter(
            post_id=pk,
            user=request.user
        ).count()
        
        dislikes_count = PostDislike.objects.filter(
            post_id=pk,
            user=request.user
        ).count()

        if likes_count > 0:
            liked = True
            percent_likes = post.likes_count() / (post.likes_count() + post.dislikes_count()) * 100 

    
        if dislikes_count > 0:
            disliked = True
            percent_dislikes = post.dislikes_count() / (post.likes_count() + post.dislikes_count()) * 100

    return render(
        request, 
        'blog/post_detail.html', 
        {'post': post, 'liked': liked, 'disliked': disliked, 
        'percent_likes': percent_likes, 'percent_dislikes': percent_dislikes}
    )

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Postagem criada com sucesso!')
            return redirect('blog:post_detail', pk=post.pk)
        else:
            logger.error('Erro na validação do formulário')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            logger.warning('Objeto post foi editado!')
            messages.success(request, 'Postagem editada com sucesso!')
            return redirect('blog:post_detail', pk=post.pk)
        else:
            logger.error('Ausência de dados em um ou mais campos do formulário. Post não adicionado')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    messages.success(request, 'Postagem publicada com sucesso!')
    return redirect('blog:post_detail', pk=pk)

def publish(self):
    self.published_date = timezone.now()
    self.save()

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.warning(request, 'Postagem removida com sucesso!')
    logger.warning('Postagem foi removida do banco de dados')
    return redirect('blog:post_list')

@login_required
def post_like(request, pk):
    likes_count = PostLike.objects.filter(
        post_id=pk,
        user=request.user
    ).count()
    
    dislikes_count = PostDislike.objects.filter(
        post_id=pk,
        user=request.user
    ).count()
    
    if likes_count == 0 and dislikes_count == 0:
        messages.success(request, 'Postagem aprovada com sucesso!')
        post_like, created = PostLike.objects.get_or_create(
            post_id=pk,
            user=request.user
        )
    else:
        messages.warning(request, 'Atenção, você já avaliou essa postagem!')
        logger.error('Tentativa em avaliar postagem negada. Já foi avaliado pelo usuário.')  
    
    return redirect('blog:post_detail', pk=pk)

@login_required
def post_dislike(request, pk):
    likes_count = PostLike.objects.filter(
        post_id=pk,
        user=request.user
    ).count()
    
    dislikes_count = PostDislike.objects.filter(
        post_id=pk,
        user=request.user
    ).count()
    
    if likes_count == 0 and dislikes_count == 0:
        messages.success(request, 'Postagem reprovada com sucesso!')

        post_dislike, created = PostDislike.objects.get_or_create(
            post_id=pk,
            user=request.user
        )
    else:
        messages.warning(request, 'Atenção, você já avaliou essa postagem!')
        logger.error('Tentativa em avaliar postagem negada. Já foi avaliado pelo usuário.')  

    return redirect('blog:post_detail', pk=pk)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('blog:post_detail', pk=post.pk)
        else:
            logger.error('Ausência de dados em um ou mais campos do formulário. Comentário não adicionado')
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(PostComment, pk=pk)
    comment.approve()
    messages.success(request, 'Comentário publicado com sucesso!')
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(PostComment, pk=pk)
    comment.delete()
    messages.warning(request, 'Comentário removido com sucesso!')
    logger.warning('Comentário removido da base de dados.')
    return redirect('blog:post_detail', pk=comment.post.pk)
