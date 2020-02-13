from django.http import HttpResponse, Http404
from django.utils import timezone
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from users.tasks import send_mail
from django.template.loader import render_to_string


@login_required
def news_list(request):
    posts = Post.objects.filter(pre_moderation=True).order_by("-published_date")
    return render(request, 'main/news_list.html', {'posts': posts})


@login_required
def post_detail(request, post_id):
    post_detail = Post.objects.get(id=post_id)
    comment_list = post_detail.comment_set.order_by('-id')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(id=post_id)         
            comment.author = request.user
            comment.save()
            subject = f"Вашу новину хтось прокоментував на FreshNews"
            message = render_to_string('users/comment.html')
            sender = "here_will_be@sender.com"
            recipients = [form.cleaned_data.get('email')]
            send_mail(subject, message, sender, recipients, fail_silently=True)
            return redirect("/")
    else:
        form = CommentForm()
    return render(request, "posts/post_detail.html", {'form': form, 'post_detail': post_detail, 'comment_list': comment_list})


