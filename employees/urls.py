from django.urls import path
from . import views
from .views import import_employees

app_name = 'employees'

urlpatterns = [
    path('', views.index, name='index'),
    path('import_employees/', import_employees, name='import_employees'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('timesheet/', views.timesheet, name='timesheet'),
]
