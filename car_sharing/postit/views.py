from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView

from .forms import AddPostItForm
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

    return redirect('car_detail', car.slug)

def delete_modal_view(request, id):
    post_it = PostIt.objects.get(id=id)

    context = {
        'post_it': post_it,
    }

    return render(request, 'postit/delete_postit_modal.html', context=context)

def create_postit_view(request, id):
    car = Car.objects.get(id=id)
    form = AddPostItForm()

    if request.method == 'POST':
        form = AddPostItForm(request.POST)
        if form.is_valid():
            post_it = form.save(commit=False)
            post_it.sender = request.user
            post_it.car = car
            post_it.save()
            return redirect('car_detail', car.slug)

    
    return render(request, 'postit/create_postit_form.html', {'form':form, 'car':car})

def delete_postit_for_everyone(request, id):
    post_it = PostIt.objects.get(id=id)
    car = post_it.car
    post_it.delete()
    

    return redirect('car_detail', car.slug)


