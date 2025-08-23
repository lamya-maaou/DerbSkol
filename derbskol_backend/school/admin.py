from django.contrib import admin
from .models import ClassRoom, Student, Teacher, Schedule, Training, TrainingEnrollment, Invoice, Payment

admin.site.register(ClassRoom)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Schedule)
admin.site.register(Training)
admin.site.register(TrainingEnrollment)
admin.site.register(Invoice)
admin.site.register(Payment)
