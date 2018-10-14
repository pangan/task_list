from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .form import TaskModelForm
from .models import Tasks

FILTER = False

def _get_categorised_tasks(tasks_data):
    todo_tasks = []
    doing_tasks = []
    done_tasks = []
    for task in tasks_data:
        if task.status == 2:
            done_tasks.append(task)
        elif task.status == 1:
            doing_tasks.append(task)
        else:
            todo_tasks.append(task)
    return todo_tasks, doing_tasks, done_tasks

@login_required
def index(request):
    user = request.user.username

    assignee_filter = False
    if 'tasklist_filter' in request.COOKIES:
        assignee_filter = (request.COOKIES.get('tasklist_filter') == 'True')

    if request.GET.get('f') == '1':
        assignee_filter = True
    elif request.GET.get('f') == '0':
        assignee_filter = False

    if assignee_filter == True:
        tasks_data = Tasks.objects.filter(assignee=user)
    else:
        tasks_data = Tasks.objects.all()

    todo_tasks, doing_tasks, done_tasks = _get_categorised_tasks(tasks_data)

    response = render(request, 'tasklist/index.html',
                  {'tasks_list': [
                      todo_tasks, doing_tasks, done_tasks]})

    response.set_cookie('tasklist_filter', assignee_filter)
    return response

@login_required
def task(request):

    if request.method == 'POST':
        task_id = request.GET.get('id')
        task_instance = None
        if task_id:
            task_instance = Tasks.objects.get(id=task_id)

        form_data = TaskModelForm(data=request.POST, instance=task_instance)
        if form_data.is_valid():

            new_task = form_data.save(commit=False)
            new_task.assignee = request.user.username
            new_task.save()
        return HttpResponseRedirect('/')

    else:
        form = TaskModelForm()
        task_id = request.GET.get('id')
        task_object = None

        if task_id:
            try:
                task_object = Tasks.objects.get(id=task_id)
            except Exception:
                pass

            form = TaskModelForm(instance=task_object)

    return render(request, 'tasklist/task.html', {'form': form, 'task_obj': task_object})


@login_required
def move_task(request):
    task_id = request.GET.get('id')

    current_status = request.GET.get('status')
    move_command = request.GET.get('move')

    task_object = Tasks.objects.filter(id=task_id, assignee=request.user.username)
    if current_status == '2' and move_command == '0':
        task_object.update(status=1, started=timezone.now(), completed=None)
    elif current_status == '1':
        if move_command == '1':
            task_object.update(status=2, completed=timezone.now())
        if move_command == '0':
            task_object.update(status=0, started=None, completed=None)
    elif current_status == '0' and move_command == '1':
        task_object.update(status=1, started=timezone.now())

    return HttpResponseRedirect('/')

@login_required
def delete_task(request):
    task_id = request.GET.get('id')
    if task_id:
        Tasks.objects.filter(id=task_id, assignee=request.user.username).delete()

    return HttpResponseRedirect('/')