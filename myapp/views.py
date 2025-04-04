from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DeleteView
from django.urls import reverse_lazy, reverse
from .forms import TaskForm, CommentForm, AttachmentForm, LoginForm
from .models import Tasks, Comments, Attachments
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('myapp:home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:login')  # Перенаправление на страницу входа
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Home view
@login_required
def home(request):
    tasks = Tasks.objects.all()
    users = User.objects.all()
    return render(request, 'myapp/home.html', {'tasks': tasks, 'users': users})

# @login_required
def task_list(request):
    tasks = Tasks.objects.all()
    return render(request, 'myapp/task_list.html', {'tasks': tasks})

# Create task view
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('myapp:task_list')
    else:
        form = TaskForm()
    return render(request, 'myapp/create_task.html', {'form': form, 'task_form': form})

# Edit task view
@login_required
def edit_task(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.user != task.user:
        raise PermissionDenied("You do not have permission to edit this task.")
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('myapp:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'myapp/edit_task.html', {'form': form, 'task_form': form, 'task': task})

# Task delete view
class TaskDeleteView(DeleteView):
    model = Tasks
    success_url = reverse_lazy('myapp:task_list')
    template_name = 'myapp/tasks_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.user:
            raise PermissionDenied("You do not have permission to delete this task.")
        return super().dispatch(request, *args, **kwargs)

# Create comment view
@login_required
def create_comment(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user  # Assign the current user
            comment.save()
            return redirect(reverse('myapp:task_detail', args=[task_id]))  # Redirect to task detail
    else:
        form = CommentForm()
    return render(request, 'myapp/create_comment.html', {'form': form, 'task': task, 'comment_form': form})

# Create attachment view
@login_required
def create_attachment(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.task = task
            # attachment.file_url = request.FILES['file_url']  # Это может вызвать ошибку, если файл не передан
            attachment.save()
            return redirect(reverse('myapp:task_detail', args=[task_id]))  # Redirect to task detail
        else:
            return render(request, 'myapp/create_attachment.html', {'form': form, 'task': task, 'attachment_form': form})
    else:
        form = AttachmentForm()
    return render(request, 'myapp/create_attachment.html', {'form': form, 'task': task, 'attachment_form': form})

# Task detail view
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    comments = Comments.objects.filter(task=task)
    attachments = Attachments.objects.filter(task=task)
    comment_form = CommentForm()
    attachment_form = AttachmentForm()

    return render(request, 'myapp/task_detail.html', {
        'task': task,
        'comments': comments,
        'attachments': attachments,
        'comment_form': comment_form,
        'attachment_form': attachment_form,
    })


