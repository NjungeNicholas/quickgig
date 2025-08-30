from rest_framework import serializers
from .models import AvailabilitySlot, Booking

class AvailabilitySlotSerializer(serializers.ModelSerializer):
    tasker_name = serializers.CharField(source="tasker.username", read_only=True)

    class Meta:
        model = AvailabilitySlot
        fields = [
            "id", "tasker", "tasker_name",
            "date", "start_time", "end_time",
            "is_booked", "created_at"
        ]
        read_only_fields = ["is_booked", "created_at"]

class BookingSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.username", read_only=True)
    tasker_name = serializers.CharField(source="tasker.username", read_only=True)
    slot_detail = AvailabilitySlotSerializer(source="availability_slot", read_only=True)
    task_name = serializers.CharField(source="task.name", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id", "client", "client_name",
            "tasker", "tasker_name",
            "task", "task_name",
            "description",
            "availability_slot", "slot_detail",
            "status", "created_at", "updated_at"
        ]
        read_only_fields = ["status", "created_at", "updated_at"]
