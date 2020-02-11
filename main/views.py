from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth.models import User

@login_required
def news_list(request):
	posts = Post.objects.all()
	return render(request, 'main/news_list.html', {'posts': posts})

def post_detail(request):
	return HttpResponse('Its works')
