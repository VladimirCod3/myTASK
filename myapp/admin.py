from django.contrib import admin
from .models import Tasks, TaskStatus, TaskPriority, Attachments, Comments, Tags, TaskTags, RelatedTasks

@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'deadline', 'user')
    list_filter = ('status', 'priority', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)

@admin.register(TaskPriority)
class TaskPriorityAdmin(admin.ModelAdmin):
    list_display = ('priority_level',)

@admin.register(Attachments)
class AttachmentsAdmin(admin.ModelAdmin):
    list_display = ('task', 'file_url', 'created_at')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'comment', 'created_at')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(TaskTags)
class TaskTagsAdmin(admin.ModelAdmin):
    list_display = ('task', 'tag')

@admin.register(RelatedTasks)
class RelatedTasksAdmin(admin.ModelAdmin):
    list_display = ('task', 'related_task')


# Register your models here.
