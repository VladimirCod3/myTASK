from django.contrib import admin
from django.urls import include, path
from myapp import views  # Import views from myapp
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('myapp.urls')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
