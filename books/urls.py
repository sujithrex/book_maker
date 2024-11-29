from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:project_pk>/chapter/new/', views.chapter_edit, name='chapter_create'),
    path('project/<int:project_pk>/chapter/<int:chapter_pk>/edit/', views.chapter_edit, name='chapter_edit'),
    path('project/<int:project_pk>/chapter/<int:chapter_pk>/delete/', views.chapter_delete, name='chapter_delete'),
    path('project/<int:project_pk>/asset/upload/', views.asset_upload, name='asset_upload'),
    path('project/<int:project_pk>/pdf/export/', views.export_pdf, name='export_pdf'),
] 