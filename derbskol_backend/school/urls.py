from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClassRoomViewSet, StudentViewSet, TeacherViewSet, ScheduleViewSet,
    TrainingViewSet, TrainingEnrollmentViewSet, InvoiceViewSet, PaymentViewSet
)

router = DefaultRouter()
router.register(r'classrooms', ClassRoomViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'trainings', TrainingViewSet)
router.register(r'training-enrollments', TrainingEnrollmentViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
