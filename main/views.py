from django.http import HttpResponse, Http404
from django.utils import timezone
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse


@login_required
def news_list(request):
    posts = Post.objects.filter(pre_moderation=True).order_by("-published_date")
    return render(request, 'main/news_list.html', {'posts': posts})


@login_required
def post_detail(request, post_id):
    post_detail = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(id=post_id)         
            comment.author = request.user
            comment.save()
            return redirect("/")
    else:
        form = CommentForm(request.POST)
    return render(request, "posts/post_detail.html", {'form': form, 'post_detail': post_detail})


