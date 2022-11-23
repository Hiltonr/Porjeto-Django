from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Task 
from .forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

 

@login_required
def tasklist(request): 

    #busca

    search = request.GET.get('search')

    if search:

        tasks = Task.objects.filter(title__icontains=search, user=request.user)   
    else:
                    #Ordenando tarefa por mais recente
        tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user)            
    
        paginatior = Paginator(tasks_list, 3)                       
        
        page = request.GET.get('page')                             
        tasks = paginatior.get_page(page)                   
        
    return render(request, 'tasks/list.html', {'tasks': tasks})  
                                                                        

         #Mostrando tarefa única

@login_required
def taskview(request, id):
    task = get_object_or_404(Task, pk=id) 
    return render(request, 'tasks/taskunica.html', {'task': task})  
     
     #Criando nova tarefa

@login_required
def novatask(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False) 
            task.done = 'doing'
            task.user = request.user
            task.save()                   
            return redirect('/')

    form = TaskForm()
    return render(request, 'tasks/novatask.html', {'form' : form })
    
    #Editando tarefa

@login_required
def edittask(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)  
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task) 
        
        if (form.is_valid()):
            task.save()
            return redirect('/')
        else:
            return render(request, 'tasks/editartask.html', {'form': form, 'task': task}) 
    
    else:
        return render(request, 'tasks/editartask.html', {'form': form, 'task': task})

    #Deletando tarefa

@login_required
def deletetask(request, id):
   task = get_object_or_404(Task, pk=id)
   task.delete() 
   messages.info(request, 'Tarefa deletada com sucesso')
   return redirect('/')
