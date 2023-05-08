from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from .models import *

# Create your views here.
def not_show_view(request, id):
    post_it = PostIt.objects.get(id=id)
    car = post_it.car
    users = car.users.all()
    not_show_post_it = PostItNotShowed(post_it=post_it, user=request.user)
    not_show_post_it.save()

    all_not_show = PostItNotShowed.objects.filter(post_it=post_it)
    if all_not_show.count() >= users.count():
        post_it.delete()

    return redirect('car_detail', car.id, car.slug)

def delete_modal_view(request, id):
    post_it = PostIt.objects.get(id=id)

    context = {
        'post_it': post_it,
    }

    return render(request, 'postit/delete_postit_modal.html', context=context)

def delete_postit_for_everyone(request, id):
    post_it = PostIt.objects.get(id=id)
    car = post_it.car
    post_it.delete()
    

    return redirect('car_detail', car.id, car.slug)


