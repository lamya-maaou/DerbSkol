from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# --- Scolarité de base ---
class ClassRoom(models.Model):
    name = models.CharField(max_length=100)          # ex: 1ère A, 3ème B
    level = models.CharField(max_length=50)          # ex: Primaire, Collège, Lycée
    year = models.CharField(max_length=9)            # ex: 2024-2025

    def __str__(self):
        return f"{self.name} ({self.year})"

class Student(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Teacher(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    subject = models.CharField(max_length=120)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"

# Emploi du temps (simple)
class Schedule(models.Model):
    DAYS = [
        (0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'),
        (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')
    ]
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=120)
    day_of_week = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

# --- Formations payantes ---
class Training(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class TrainingEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'training')

# --- Finance ---
class Invoice(models.Model):
    STATUS = [
        ('DRAFT', 'Draft'),
        ('ISSUED', 'Issued'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]
    number = models.CharField(max_length=50, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default='ISSUED')
    issued_at = models.DateTimeField(default=timezone.now)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)

    def __str__(self):
        return self.number

class Payment(models.Model):
    METHOD = [('CASH','Cash'), ('CARD','Card'), ('BANK','Bank'), ('ONLINE','Online')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=10, choices=METHOD, default='CASH')
    paid_at = models.DateTimeField(default=timezone.now)
    note = models.CharField(max_length=255, blank=True)

    # Cas d’usage: on enregistre un paiement → on génère automatiquement une facture
    # via un signal post_save (voir signals.py)
