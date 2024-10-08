from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, StarRating, Applause
from .forms import PostForm, CommentForm 
from django.db.models import Avg


def home(request):
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'create_comment.html', {'form': form})


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # Calculate average rating
#     avg_rating = post.star_ratings.aggregate(Avg('rating'))['rating__avg']
    
#     context = {
#         'post': post,
#         'avg_rating': avg_rating,  # Pass it to the template
#     }
#     return render(request, 'blog/post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/delete_post.html', {'post': post})

@login_required
def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    return redirect('post_detail', pk=pk)

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    liked = created
    if not created:
        like.delete()
    total_likes = post.likes.count()
    return JsonResponse({'total_likes': total_likes, 'liked': liked})

@login_required
def star_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    rating = int(request.POST.get('rating'))
    StarRating.objects.update_or_create(post=post, user=request.user, defaults={'rating': rating})
    average_rating = post.star_ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    return JsonResponse({'average_rating': average_rating})

@login_required
def applaud_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    applause, created = Applause.objects.get_or_create(post=post, user=request.user)
    applauded = created
    if not created:
        applause.delete()
    total_applauses = post.applauses.count()
    return JsonResponse({'total_applauses': total_applauses, 'applauded': applauded})
