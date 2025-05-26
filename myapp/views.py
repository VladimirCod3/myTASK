from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import TaskForm, CommentForm, AttachmentForm, LoginForm, UserForm, ProfileForm
from .models import Tasks, Comments, Attachments


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('myapp:home')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Профиль создаётся через сигнал post_save, если он настроен
            messages.success(request, 'Регистрация прошла успешно! Войдите в систему.')
            return redirect('myapp:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    tasks = Tasks.objects.filter(user=request.user)
    users = User.objects.all()
    return render(request, 'myapp/home.html', {'tasks': tasks, 'users': users})


@login_required
def task_list(request):
    tasks = Tasks.objects.filter(user=request.user)
    return render(request, 'myapp/task_list.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Задача успешно создана!')
            return redirect('myapp:task_list')
    else:
        form = TaskForm()
    return render(request, 'myapp/create_task.html', {'form': form})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if task.user != request.user:
        raise PermissionDenied("У вас нет прав редактировать эту задачу.")
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('myapp:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'myapp/edit_task.html', {'form': form, 'task': task})


class TaskDeleteView(DeleteView):
    model = Tasks
    success_url = reverse_lazy('myapp:task_list')
    template_name = 'myapp/tasks_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != request.user:
            raise PermissionDenied("У вас нет прав удалять эту задачу.")
        return super().dispatch(request, *args, **kwargs)


@login_required
def create_comment(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    if task.user != request.user:
        raise PermissionDenied("У вас нет прав комментировать эту задачу.")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('myapp:task_detail', task_id=task_id)
    else:
        form = CommentForm()
    return render(request, 'myapp/create_comment.html', {'form': form, 'task': task})


@login_required
def create_attachment(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    if task.user != request.user:
        raise PermissionDenied("У вас нет прав добавлять вложения к этой задаче.")
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.task = task
            attachment.save()
            messages.success(request, 'Вложение успешно добавлено!')
            return redirect('myapp:task_detail', task_id=task_id)
        else:
            messages.error(request, 'Ошибка при загрузке вложения.')
    else:
        form = AttachmentForm()
    return render(request, 'myapp/create_attachment.html', {'form': form, 'task': task})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Tasks.objects.select_related('status', 'priority', 'user'), pk=task_id)
    if task.user != request.user:
        raise PermissionDenied("У вас нет прав просматривать эту задачу.")
    comments = Comments.objects.filter(task=task).select_related('user')
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


@login_required
def profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'myapp/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('myapp:profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'form': profile_form,
        'profile': profile,
    }
    return render(request, 'myapp/edit_profile.html', context)

