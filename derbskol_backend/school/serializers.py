from rest_framework import serializers
from .models import Student, ClassRoom, Teacher, Schedule, Training, TrainingEnrollment, Invoice, Payment

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class_room = ClassRoomSerializer(read_only=True)
    class_room_id = serializers.PrimaryKeyRelatedField(
        source='class_room', queryset=ClassRoom.objects.all(), write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Student
        fields = ['id','first_name','last_name','email','enrollment_date','class_room','class_room_id']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'

class TrainingEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingEnrollment
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['number','status','issued_at','pdf_file']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
