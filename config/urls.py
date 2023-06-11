"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('add_habit/', views.add_habit, name='add_habit'),
    path('habit_detail/<int:pk>', views.habit_detail, name='habit_detail'),
    path('delete_habit/<int:pk>', views.delete_habit, name='delete_habit'),
    path('edit_habit/<int:pk>', views.edit_habit, name='edit_habit'),
    path('habit_detail/<int:pk>/add_tracker/', views.add_tracker, name="add_tracker"),
    path('habit_detail/<int:pk>/edit_tracker/', views.edit_tracker, name="edit_tracker"),
    path('habit_detail/<int:pk>/delete_tracker/', views.edit_tracker, name="edit_tracker"),
    path('habit_detail/<int:pk>/tracker_detail/', views.tracker_detail, name="tracker_detail"),
    path('account_detail', views.account_detail, name="account_detail"),
    path('habit_detail/<int:pk>/add_observer', views.add_observer, name="add_observer"),
    path('delete_observer', views.delete_observer, name="delete_observer"),
    path('no_permission', views.no_permission, name="no_permission"),
    path("habit_detail/<int:pk>/tracker_chart", views.tracker_chart, name="tracker_chart")
]
