from datetime import timedelta, date

from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=255, default='None')
    department = models.CharField(max_length=255, default='Транспортный участок')
    position = models.CharField(max_length=255, default='Водитель погрузчика')
    quality = models.CharField(max_length=255, default='3 разряд')
    birth_date = models.DateField(default='None')
    age = models.IntegerField(default='18')
    male = models.CharField(max_length=10, default='М')
    education = models.CharField(max_length=255, default='None')
    experience = models.IntegerField(default=2)
    extra = models.FloatField(default=0.02)
    address = models.CharField(max_length=255, default='None')
    instruction_date = models.DateField()

    INSTRUCTION_TYPES = (
        ('primary', 'Первичный'),
        ('recurring', 'Повторный'),
        ('ad_hoc', 'Внеплановый'),
    )

    instruction_type = models.CharField(max_length=10, choices=INSTRUCTION_TYPES)

    def calculate_next_training_date(self):
        if self.instruction_type == 'recurring':
            # Определяем следующую дату инструктажа
            current_date = date.today()
            last_training_date = self.instruction_date

            # Проверяем, прошло ли уже 3 месяца с последнего инструктажа
            while last_training_date < current_date:
                last_training_date += timedelta(days=90)  # Добавляем 90 дней (3 месяца)

            return last_training_date

        # Если тип инструктажа не является 'recurring', возвращаем None или другое значение,
        # в зависимости от вашей логики приложения
        return None
    def __str__(self):
        return self.full_name

class WorkClothes(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField()

class Contract(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class Training(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training_type = models.CharField(max_length=200)
    last_training_date = models.DateField()
    next_training_date = models.DateField()
