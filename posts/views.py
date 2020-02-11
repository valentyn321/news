from django.shortcuts import render
from django.http import HttpResponse
from main.models import Post
from .forms import PostForm

# @login_required
def post_creation(request):
	form = PostForm()
	return render(request, 'posts/post_creation.html', {'form': form})
