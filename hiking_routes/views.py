from django.shortcuts import render, redirect, get_object_or_404

from .models import Post


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-pk')
        return render(
            request,
            'hiking_routes/index.html',
            {
                'posts': posts
            }
        )
    return redirect('/')

def post_detail(request, pk):
    post = Post.objects.get(pk = pk)
    return render(
        request,
        'hiking_routes/post_detail.html',
        {
            'post': post
        }
    )

def new_post(request):
    return render(
        request,
        'hiking_routes/new_post.html'
    )

def create_post(request):
    return None

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(
        request,
        'hiking_routes/edit_post.html',
        {
            'post': post
        }
    )

def update_post(request, pk):
    return None

def delete_post(request, pk):
    deleted_post = Post.objects.get(id=id)
    deleted_post.delete()
    return redirect('/routes/')
