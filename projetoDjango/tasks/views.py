from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

@login_required
def taskList(request):
    search = request.GET.get('search')
    filter = request.GET.get('filter')

    if search:
        tasks = Task.objects.filter(title__icontains=search, user=request.user)
    elif filter:
        tasks = Task.objects.filter(done=filter, user=request.user)
    else:
        tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user)
        paginator = Paginator(tasks_list, 3)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)

    return render(request, 'tasks/list.html', {'tasks': tasks, 'filter': filter})

@login_required
def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.user != task.user:
        messages.info(request, 'Você não tem permissão para visualizar essa tarefa!')
        return redirect('/')
    else:
        return render(request, 'tasks/task.html', {'task': task})

@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.user = request.user
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})
    
@login_required
def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    if task.user != request.user:
        messages.info(request, 'Você não tem permissão para editar essa tarefa!')
        return redirect('/')
    else:
        form = TaskForm(instance=task)
        if(request.method == 'POST'):
            form = TaskForm(request.POST, instance=task)
            if(form.is_valid()):
                task.save()
                return redirect('/')
            else:
                return render(request, 'tasks/edittask.html', {'form': form, 'task': task})
        else:
            return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

@login_required
def changeStatus(request, id):
    task = get_object_or_404(Task, pk=id)
    if task.user != request.user:
        messages.info(request, 'Você não tem permissão para editar essa tarefa!')
        return redirect('/')
    else:
        if(task.done == 'doing'):
            task.done = 'done'
        else:
            task.done = 'doing'
        task.save()
        return redirect('/')

@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    if task.user != request.user:
        messages.info(request, 'Você não tem permissão para excluir essa tarefa!')
        return redirect('/')
    else:
        task.delete()

        messages.info(request, 'Tarefa deletada com sucesso.')

        return redirect('/')

def helloWorld(request):
    return HttpResponse('Hello World!')

def yourName(request, name):
    return render(request, 'tasks/yourname.html', {'name':name})