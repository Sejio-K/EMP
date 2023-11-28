from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, WorkClothes, Contract
from .forms import EmployeeForm
from datetime import datetime, date
import pandas as pd

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})



def add_employee(request):
    form = EmployeeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    return render(request, 'employees/add_employee.html', {'form': form})



def import_employees(request):
    if request.method == 'POST':
        try:
            # Получить загруженный файл Excel
            excel_file = request.FILES['excel_file']

            # Загрузить данные из файла в pandas
            df = pd.read_excel(excel_file)

            # Преобразовать данные и сохранить в базу данных
            for index, row in df.iterrows():
                employee = Employee.objects.create(
                    full_name=row['Сотрудник'],
                    department=row['Подразделение'],
                    position=row['Профессия (должность)'],
                    quality=row['Разряд'],
                    birth_date=row['Дата рождения'],
                    age=row['Возраст (лет)'],
                    male=row['Пол'],
                    education=row['Образование'],
                    experience=row['Стаж (лет)'],
                    extra=row['% за стаж'],
                    address=row['Адрес']
                )

        except Exception as e:
            # Обработка ошибок при загрузке данных из файла Excel
            return render(request, 'import_error.html', {'error': str(e)})

    return render(request, 'import_employees.html')

def index(request):
    current_date = datetime.now().date()
    next_training_employee = Employee.objects.filter(instruction_date=current_date).first()
    if next_training_employee:
        next_training_date = next_training_employee.calculate_next_training_date()
    else:
        next_training_date = None
    work_clothes_employee = WorkClothes.objects.filter(issue_date=current_date).first()
    contract_employee = Employee.objects.filter(contract__end_date=current_date).first()
    birthday_employee = Employee.objects.filter(birth_date__month=current_date.month, birth_date__day=current_date.day).first()

    return render(request, 'index.html', {
        'current_date': current_date,
        'next_training_employee': next_training_employee,
        'work_clothes_employee': work_clothes_employee,
        'contract_employee': contract_employee,
        'birthday_employee': birthday_employee
    })




def timesheet(request):
    employees = Employee.objects.all()
    return render(request, 'employees/timesheet.html', {'employees': employees})