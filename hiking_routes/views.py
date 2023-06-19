from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Post, Participate


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
    if request.method == 'POST' and request.user.is_authenticated:
        post = Post()
        post.title = request.POST['title']
        post.author = request.user
        post.content = request.POST['content']
        if request.FILES.get('image') is not None:
            post.image = request.FILES['image']
        post.date = request.POST['date']
        post.max_member = request.POST['max_member']
        post.start_point = request.POST['start_point']
        post.end_point = request.POST['end_point']

        post.save()

        return redirect(
            'detail',
            post.pk
        )
    return redirect('/')

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user and request.user.is_authenticated:
        return render(
            request,
            'hiking_routes/edit_post.html',
            {
                'post': post
            }
        )
    else:
        redirect(
            'detail',
            pk
        )

def update_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author == request.user and request.user.is_authenticated:
        post.title = request.POST['title']
        post.author = request.user
        post.content = request.POST['content']
        if request.FILES.get('image') is not None:
            post.image = request.FILES['image']
        post.date = request.POST['date']
        post.max_member = request.POST['max_member']
        post.start_point = request.POST['start_point']
        post.end_point = request.POST['end_point']

        post.save()

    return redirect('detail', pk)

def delete_post(request, pk):
    deleted_post = Post.objects.get(pk=pk)
    deleted_post.delete()
    return redirect('/routes/')

def participate(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user.is_authenticated and request.user != post.author:
        parts = Participate.objects.filter(post=post)
        is_parted = parts.filter(author=request.user)
        if is_parted:
            messages.error(request, "이미 참여되었습니다.")
            return redirect('detail', pk)
        if is_parted.count() >= post.max_member:
            messages.error(request, "참여인원을 초과했습니다.")
            return redirect('detail', pk)
        part = Participate()
        part.post = post
        part.author = request.user
        part.save()
        messages.info(request, "참여가 완료되었습니다.")
        return redirect('detail', pk)
    messages.error(request, "참여할 수 없습니다")
    return redirect('detail', pk)

