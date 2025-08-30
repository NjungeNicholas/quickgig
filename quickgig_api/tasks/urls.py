from django.urls import path
from .views import (
    AvailabilitySlotListCreateView, AvailabilitySlotDetailView,
    BookingListCreateView, BookingDetailView, DailyAvailabilitySlotView,client_bookings, tasker_bookings
)

urlpatterns = [
    # Availability
    path("slots/", AvailabilitySlotListCreateView.as_view(), name="slot-list"),
    path("slots/<int:pk>/", AvailabilitySlotDetailView.as_view(), name="slot-detail"),
    path("slots/daily/", DailyAvailabilitySlotView.as_view(), name="slot-daily"),

    # Bookings
    path("bookings/", BookingListCreateView.as_view(), name="booking-list"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    # Client Bookings
    path("bookings/client/", client_bookings, name="client-bookings"),
    # Tasker Bookings
    path("bookings/tasker/", tasker_bookings, name="tasker-bookings"),
]

"""
Tasks API Endpoints
===================

Availability Slots
------------------
- GET    /api/tasks/slots/
    List all availability slots.
- GET   /api/tasks/slots/?tasker=<tasker_id>
    List all availability slots for a specific tasker.
- POST   /api/tasks/slots/
    Create a new availability slot for the authenticated tasker.
- GET    /api/tasks/slots/<int:pk>/
    Retrieve details of a specific availability slot.
- PATCH  /api/tasks/slots/<int:pk>/
    Partially update a specific availability slot (owner only).
- PUT    /api/tasks/slots/<int:pk>/
    Fully update a specific availability slot (owner only).
- DELETE /api/tasks/slots/<int:pk>/
    Delete a specific availability slot (owner only).
- POST   /api/tasks/slots/daily/
    Bulk create multiple availability slots for the authenticated tasker (daily or weekly).

Bookings
--------
- GET    /api/tasks/bookings/
    List all bookings (authenticated users).
- POST   /api/tasks/bookings/
    Create a new booking (authenticated users).
- GET    /api/tasks/bookings/<int:pk>/
    Retrieve details of a specific booking (tasker or client).
- PATCH  /api/tasks/bookings/<int:pk>/
    Partially update the status of a booking (tasker or client).
- PUT    /api/tasks/bookings/<int:pk>/
    Fully update the status of a booking (tasker or client).
- DELETE /api/tasks/bookings/<int:pk>/
    Cancel a booking (only clients can cancel).
- GET    /api/tasks/bookings/client/
    Get user's bookings as client (optional).
- GET    /api/tasks/bookings/tasker/
    Get user's bookings as tasker (optional).

Notes
-----
- All endpoints require authentication unless otherwise specified.
- Permissions are enforced so only owners can modify or delete their slots/bookings.
- Bulk slot creation returns a multi-status response if some slots fail validation.
"""
