from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
#from django.http import Http404
from django.urls import reverse
from .models import Task
from .forms import TaskForm


@login_required(login_url='user-login')
def task_list(request):
    tasks = request.user.task_set.all().order_by('-created')
    form = TaskForm()
    context = {'tasks': tasks, 'form': form}
    return render(request, 'task-list.html', context)


'''
@login_required(login_url='user-login')
def update_task(request, id):
    task = get_object_or_404(Task, id=id)
    form = TaskForm(instance=task)
    context = {'form': form}
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect(reverse('task-list'))
    return render(request, 'update-task.html', context)
    
@login_required(login_url='user-login')
def remove_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.delete()
        return redirect(reverse('task-list'))
    return render(request, 'remove-task.html')
'''


#api calls
def add_task(request):
    response_dict = {}
    if request.method == 'POST' and request.user.is_authenticated:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            request.user.task_set.add(task)
            response_dict['status'] = 'success'
            response_dict['id'] = task.id 
            response_dict['title'] = task.title
        else:
            response_dict['status'] = 'error'
    else:
        response_dict['status'] = 'denied'
    return JsonResponse(response_dict)


def update_task(request):
    response_dict = {}
    if request.method == 'POST' and request.user.is_authenticated:
        id = request.POST.get('id')
        title = request.POST.get('title')
        try:
            task = Task.objects.get(id=id)
            task.title = title
            task.save()
            response_dict['status'] = 'success'
            response_dict['title'] = task.title
            response_dict['complete'] = task.completed
        except:
            response_dict['status'] = 'error'
    else:
        response_dict['status'] = 'denied'
    return JsonResponse(response_dict)


def remove_task(request):
    response_dict = {}
    if request.method == 'POST' and request.user.is_authenticated:
        id = request.POST.get('id')
        try:
            Task.objects.get(id=id).delete()
            response_dict['status'] = 'success'
        except:
            response_dict['status'] = 'error'
    else:
        response_dict['status'] = 'denied'
    return JsonResponse(response_dict)


def complete_task(request):
    response_dict = {}
    if request.method == 'POST' and request.user.is_authenticated:
        id = request.POST.get('id')
        comp = request.POST.get('complete')
        print(type(comp))
        try:
            task = Task.objects.get(id=id)
            task.completed = True if comp=='0' else False
            task.save()
            response_dict['status'] = 'success'
        except:
            response_dict['status'] = 'error'
    else:
        response_dict['status'] = 'deneid'
    return JsonResponse(response_dict)
            
