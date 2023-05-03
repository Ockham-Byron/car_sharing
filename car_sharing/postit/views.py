from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def not_show_view(request, id):
    post_it = PostIt.objects.get(id=id)
    not_show_post_it = PostItNotShowed(post_it=post_it, user=request.user)
    not_show_post_it.save()

    return redirect('/')