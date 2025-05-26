from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Встроенные URL для аутентификации (вход, выход, смена пароля и т.д.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Основные маршруты вашего приложения
    path('', include('myapp.urls')),

    # Явный маршрут для выхода с перенаправлением на главную страницу
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

# Отдача медиа-файлов при DEBUG=True (только для разработки)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


