from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Student, ClassRoom, Teacher, Schedule, Training, TrainingEnrollment, Invoice, Payment
from .serializers import (
    StudentSerializer, ClassRoomSerializer, TeacherSerializer, ScheduleSerializer,
    TrainingSerializer, TrainingEnrollmentSerializer, InvoiceSerializer, PaymentSerializer
)

class ClassRoomViewSet(ModelViewSet):
    queryset = ClassRoom.objects.all().order_by('-year','name')
    serializer_class = ClassRoomSerializer

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all().order_by('-enrollment_date')
    serializer_class = StudentSerializer

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all().order_by('last_name')
    serializer_class = TeacherSerializer

class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all().order_by('class_room','day_of_week','start_time')
    serializer_class = ScheduleSerializer

class TrainingViewSet(ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

class TrainingEnrollmentViewSet(ModelViewSet):
    queryset = TrainingEnrollment.objects.all()
    serializer_class = TrainingEnrollmentSerializer

class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all().order_by('-issued_at')
    serializer_class = InvoiceSerializer

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all().order_by('-paid_at')
    serializer_class = PaymentSerializer
    # Quand on crée un Payment => le signal crée une Invoice PAID automatiquement
