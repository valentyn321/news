from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Post
from main.forms import PostForm
from django.utils import timezone
from .decorators import unauth_user, allowed_groups
from django.contrib.auth.decorators import login_required


@login_required
@allowed_groups(disallowed_roles=['user'])
def post_creation(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.pre_moderation = True
            post.save()
            return redirect("/")
    else:
        form = PostForm()
    return render(request, 'posts/post_creation.html', {'form': form})

@login_required
def post_moderation(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.pre_moderation = False
            post.save()
            return redirect("/")
    else:
        form = PostForm()
    return render(request, 'posts/post_creation.html', {'form': form})



# @login_required
# def leave_comment(request, post_id):
#     try: 
#         post_detail = Post.objects.get(id=post_id)
#     except:
#         raise Http404("Стаття не знайдена!")

#     post_detail.comment_set.create(author=request.POST['name'], text=request.POST['text'])

#     return