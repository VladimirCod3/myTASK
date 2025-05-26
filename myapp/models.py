from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html


class TaskStatus(models.Model):
    status = models.CharField(max_length=50, verbose_name='Статус')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class TaskPriority(models.Model):
    priority_level = models.CharField(max_length=50, verbose_name='Приоритет')

    def __str__(self):
        return self.priority_level

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'


class Tasks(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    status = models.ForeignKey(
        TaskStatus, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='Статус', related_name='tasks'
    )
    priority = models.ForeignKey(
        TaskPriority, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='Приоритет', related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='Срок выполнения')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь',
        related_name='tasks', db_index=True
    )

    def __str__(self):
        return self.title

    @property
    def tags(self):
        return Tags.objects.filter(tasktags__task=self)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']


class Attachments(models.Model):
    task = models.ForeignKey(
        Tasks, on_delete=models.CASCADE, verbose_name='Задача', related_name='attachments'
    )
    file = models.FileField(upload_to='attachments/', verbose_name='Файл')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.file.name if self.file else 'Без файла'

    def file_url(self):
        if self.file:
            return format_html('<a href="{}" target="_blank">{}</a>', self.file.url, self.file.name)
        return 'Нет файла'

    file_url.short_description = 'Файл'

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'


class Comments(models.Model):
    task = models.ForeignKey(
        Tasks, on_delete=models.CASCADE, verbose_name='Задача', related_name='comments'
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь'
    )
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        if self.comment:
            return (self.comment[:75] + '...') if len(self.comment) > 75 else self.comment
        return ''

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']


class Tags(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class TaskTags(models.Model):
    task = models.ForeignKey(
        Tasks, on_delete=models.CASCADE, verbose_name='Задача', related_name='task_tags'
    )
    tag = models.ForeignKey(
        Tags, on_delete=models.CASCADE, verbose_name='Тег', related_name='tag_tasks'
    )

    class Meta:
        unique_together = (('task', 'tag'),)
        verbose_name = 'Тег задачи'
        verbose_name_plural = 'Теги задач'

    def __str__(self):
        return f"Тег '{self.tag.name}' для задачи '{self.task.title}'"


class RelatedTasks(models.Model):
    task = models.ForeignKey(
        Tasks, on_delete=models.CASCADE, related_name='related_task_set', verbose_name='Задача'
    )
    related_task = models.ForeignKey(
        Tasks, on_delete=models.CASCADE, related_name='related_to_task',
        null=True, blank=True, verbose_name='Связанная задача'
    )

    class Meta:
        unique_together = (('task', 'related_task'),)
        verbose_name = 'Связанная задача'
        verbose_name_plural = 'Связанные задачи'

    def __str__(self):
        return f"Связанная задача для '{self.task.title}'"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='profile'
    )
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True, verbose_name='Аватар'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    location = models.CharField(max_length=100, blank=True, verbose_name='Местоположение')

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)

