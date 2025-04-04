from django.db import models
from django.contrib.auth.models import User

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
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Статус')
    priority = models.ForeignKey(TaskPriority, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Приоритет')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='Срок выполнения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь', db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class Attachments(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Задача')
    file_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='URL файла')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.file_url

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'

class Comments(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Задача')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Tags(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class TaskTags(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Задача')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Тег')

    class Meta:
        unique_together = (('task', 'tag'),)
        verbose_name = 'Тег задачи'
        verbose_name_plural = 'Теги задач'

    def __str__(self):
        return f"Tag {self.tag.name} for Task {self.task.title}"

class RelatedTasks(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        related_name='related_task_set',
        verbose_name='Задача'
    )
    related_task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        related_name='related_to_task',
        null=True,
        blank=True,
        verbose_name='Связанная задача'
    )

    class Meta:
        unique_together = (('task', 'related_task'),)
        verbose_name = 'Связанная задача'
        verbose_name_plural = 'Связанные задачи'

    def __str__(self):
        return f"Related Task for {self.task.title}"


