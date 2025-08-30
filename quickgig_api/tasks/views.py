from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import AvailabilitySlot, Booking, BookingService
from .serializers import AvailabilitySlotSerializer, BookingSerializer
from accounts.permissions import (    
    IsOwnerOrReadOnly,
    IsTaskerOrClient,
)
from rest_framework.decorators import api_view, permission_classes


class AvailabilitySlotListCreateView(generics.ListCreateAPIView):
    """List all slots or creates a new availability slot"""
    queryset = AvailabilitySlot.objects.all()
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = AvailabilitySlot.objects.all()
        tasker_id = self.request.query_params.get("tasker")

        if tasker_id:
            queryset = queryset.filter(tasker_id=tasker_id)

        return queryset
    
    def create(self, request, *args, **kwargs):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        tasker = request.user

        if AvailabilitySlot.objects.filter(start_time=start_time, end_time=end_time, tasker=tasker).exists():
            return Response(
                {"detail": "A slot with the same start and end time already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(tasker=tasker)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DailyAvailabilitySlotView(generics.CreateAPIView):
    """Taskers can create multiple availability slots at once (daily or weekly)"""
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        slots_data = request.data.get('slots', [])
        tasker = request.user
        created_slots = []
        errors = []

        for slot_data in slots_data:
            start_time = slot_data.get('start_time')
            end_time = slot_data.get('end_time')

            if AvailabilitySlot.objects.filter(start_time=start_time, end_time=end_time, tasker=tasker).exists():
                errors.append(
                    {"detail": f"A slot with the same start and end time already exists: {start_time} - {end_time}."}
                )
                continue

            serializer = self.get_serializer(data=slot_data)
            if serializer.is_valid():
                serializer.save(tasker=tasker)
                created_slots.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response(
                {"created_slots": created_slots, "errors": errors},
                status=status.HTTP_207_MULTI_STATUS
            )
        return Response(created_slots, status=status.HTTP_201_CREATED)

class AvailabilitySlotDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View, update, or delete a specific slot"""
    queryset = AvailabilitySlot.objects.all()
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        try:
            availabilitySlot = AvailabilitySlot.objects.get(id=kwargs['pk'])
            serializer = self.get_serializer(availabilitySlot, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except AvailabilitySlot.DoesNotExist:
            return Response(
                {"detail": "Slot not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            availabilitySlot = AvailabilitySlot.objects.get(id=kwargs['pk'])
            availabilitySlot.delete()
            return Response(
                {"detail": "Slot deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except AvailabilitySlot.DoesNotExist:
            return Response(
                {"detail": "Slot not found"},
                status=status.HTTP_404_NOT_FOUND
            )
class BookingListCreateView(generics.ListCreateAPIView):
    """List all bookings or create a new booking"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

    def perform_create(self, serializer):
        data = serializer.validated_data
        booking = BookingService.create_booking(
            client=self.request.user,
            tasker=data["tasker"],
            task=data["task"],
            availability_slot_id=data["availability_slot"].id,
            description=data["description"]
        )
        # Save the booking instance using the serializer
        serializer.instance = booking

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View, update, or cancel a booking"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskerOrClient]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), IsTaskerOrClient()]
        return [permissions.IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        try:
            booking = self.get_object()
            taskstatus = request.data.get("status")
            BookingService.update_booking_status(booking, taskstatus)
            serializer = self.get_serializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        """Cancel booking instead of hard delete"""
        booking = self.get_object()
        cancelled = BookingService.cancel_booking(booking)
        serializer = self.get_serializer(cancelled)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Client Bookings
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def client_bookings(request):
    """Get bookings where user is the client"""
    bookings = Booking.objects.filter(client=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Tasker Bookings
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def tasker_bookings(request):
    """Get bookings where user is the tasker"""
    bookings = Booking.objects.filter(tasker=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)