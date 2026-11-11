from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('student/add/', views.student_create, name='student_create'),
    path('student/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('student/<int:pk>/fee-voucher/', views.generate_fee_voucher, name='fee_voucher'),
    path('logout/', views.logout, name='logout'),
]
