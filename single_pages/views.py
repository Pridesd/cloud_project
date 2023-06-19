from django.shortcuts import render, redirect

from hiking_routes.models import Post, Participate


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        recent_post = Post.objects.filter(author=request.user)
        recent_post = recent_post.order_by('-pk')[0:5]

        parti = Participate.objects.filter(author=request.user).order_by('-pk')
        participated_list = []
        for p in parti:
            participated_list.append(p.post)

        return render(
            request,
            'single_pages/index.html',
            {
                'recent_post': recent_post,
                'participated_list': participated_list
            }
        )
    else:
        return render(
            request,
            'single_pages/index.html'
        )