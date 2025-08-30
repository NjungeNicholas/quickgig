from django.db import models, transaction
from django.conf import settings
from services.models import Service
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class AvailabilitySlot(models.Model):
    """Availability slot for a tasker."""
    tasker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_tasker': True}, related_name='availability_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('start_time', 'end_time')
        ordering = ['date', 'start_time']

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('End time must be after start time.')
        
        if self.date < timezone.now().date():
            raise ValidationError('Cannot create availability for past dates.')

    def save(self, *args, **kwargs):
        if not self.pk:  # Only call full_clean for new objects
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tasker}, {self.date}, {self.start_time}, {self.end_time}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    """A booking task that links a client with a tasker and an availability slot"""
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_client': True}, related_name='client_bookings')
    tasker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_tasker': True}, related_name='tasker_bookings')
    task = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    description = models.TextField()
    availability_slot = models.OneToOneField(AvailabilitySlot, on_delete=models.CASCADE, related_name='booking')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['availability_slot__date', 'availability_slot__start_time']

    def __str__(self):
        return f"{self.client} -> {self.tasker} on {self.date} at {self.start_time}"

    # Properties to access availability slot details
    @property
    def date(self):
        return self.availability_slot.date

    @property
    def start_time(self):
        return self.availability_slot.start_time

    @property
    def end_time(self):
        return self.availability_slot.end_time
    
    def clean(self):
        """Ensure that the selected task is one of the tasker's skills"""
        if not self.tasker.taskerprofile.skills.filter(id=self.task.id).exists():
            raise ValidationError(f"{self.tasker} does not offer the service {self.task}.")
    

class BookingService:
    """ services to handle bookings"""

    @staticmethod
    def get_available_slots(tasker=None, date=None, task=None):
        """Get available slots for a tasker on a specific date"""
        if not tasker or not date:
            return AvailabilitySlot.objects.none()
        
        slots = AvailabilitySlot.objects.filter(tasker=tasker, date=date, is_booked=False)

        return slots
    
    @staticmethod
    @transaction.atomic
    def create_booking(client, tasker, task, availability_slot_id, description):
        """Create a new booking"""
        try:
            # Get and lock the availability slot
            availability_slot = AvailabilitySlot.objects.select_for_update().get(
                id=availability_slot_id
            )

            if availability_slot.is_booked:
                raise ValidationError('Availability slot is already booked.')

            booking = Booking.objects.create(
                client=client,
                tasker=tasker,
                task=task,
                availability_slot=availability_slot,
                description=description,
                status='confirmed'
            )

            # mark the availability slot as booked
            availability_slot.is_booked = True
            availability_slot.save()

            return booking
        except AvailabilitySlot.DoesNotExist:
            raise ValidationError("Availability slot not found")
        
    @staticmethod
    @transaction.atomic
    def cancel_booking(booking):
        """Cancel a booking"""
        try:
            booking = Booking.objects.select_for_update().get(
                id=booking.id
            )
            # only allow cancellation of confirmed bookings
            if booking.status != 'confirmed':
                raise ValidationError(f"Cannot cancel booking with status: {booking.status}")
            
            booking.status = 'cancelled'
            booking.availability_slot.is_booked = False

            booking.availability_slot.save()
            booking.save()
            return booking
        except Booking.DoesNotExist:
            raise ValidationError("Booking not found")
        
    @staticmethod
    @transaction.atomic
    def update_booking_status(booking, status):
        """Update the status of a booking"""
        try:
            booking.status = status
            booking.save()
            return booking
        except Exception as e:
            raise ValidationError(f"Error updating booking status: {e}")

    @staticmethod
    def get_tasker_bookings(tasker):
        """Get all bookings for a specific tasker"""
        if not tasker:
            return Booking.objects.none()
        return Booking.objects.filter(tasker=tasker)
    
    @staticmethod
    def get_client_bookings(client):
        """Get all bookings for a specific client"""
        if not client:
            return Booking.objects.none()
        return Booking.objects.filter(client=client)

# Booking management
class AvailabilityManager:
    """Functions to create availability slots easily"""

    @staticmethod
    def create_daily_slots(tasker, date, start_hour, end_hour, slot_duration_hours=1):
        """Create daily availability slots for a tasker"""
        slots_created = []
        current_hour = start_hour
        
        while current_hour + slot_duration_hours <= end_hour:
            start_time = datetime.time(current_hour, 0)
            end_time = datetime.time(current_hour + slot_duration_hours, 0)
            
            slot, created = AvailabilitySlot.objects.get_or_create(
                tasker=tasker,
                date=date,
                start_time=start_time,
                defaults= {
                    'end_time': end_time,
                    'is_booked': False
                }
            )
            
            if created:
                slots_created.append(slot)
            
            current_hour += slot_duration_hours
            
        return slots_created
    
    @staticmethod
    def create_weekly_slots(tasker, start_date, start_hour, end_hour, slot_duration_hours, num_weeks=1, work_days=[0,1,2,3,4,5,6]):
        """
        Create weekly availability slots for a tasker
        """
        slots_created = []
        for week in range(num_weeks):
            for day in work_days:
                date = start_date + datetime.timedelta(weeks=week, days=day)
                slots = AvailabilityManager.create_daily_slots(
                    tasker=tasker,
                    date=date,
                    start_hour=start_hour,
                    end_hour=end_hour,
                    slot_duration_hours=slot_duration_hours
                )
                slots_created.extend(slots)
        return slots_created

@receiver(post_save, sender=Booking)
def mark_slot_as_booked(sender, instance, created, **kwargs):
    """Automatically mark availability slot as booked when booking is created"""
    if created and instance.status == 'confirmed':
        # Use update() to avoid calling save() and triggering clean()
        AvailabilitySlot.objects.filter(id=instance.availability_slot.id).update(is_booked=True)

@receiver(post_save, sender=Booking)
def handle_booking_cancellation(sender, instance, **kwargs):
    """Handle slot availability when booking is cancelled"""
    if instance.status == 'cancelled':
        AvailabilitySlot.objects.filter(id=instance.availability_slot.id).update(is_booked=False)