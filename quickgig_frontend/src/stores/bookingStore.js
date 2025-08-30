import { create } from "zustand";
import * as bookingService from "../../src/services/bookingService";

const useBookingStore = create((set) => ({
  bookings: [],
  slots: [],
  loading: false,
  error: null,

  // Get clientId safely from localStorage
  getClientId: () => {
    try {
      const authData = JSON.parse(localStorage.getItem("user"));
      return authData?.id || null;
    } catch (e) {
      console.error("Failed to parse user:", e);
      return null;
    }
  },

  // Fetch tasker's availability slots
  fetchTaskerSlots: async (taskerId) => {
    set({ loading: true });
    try {
      const res = await bookingService.getTaskerSlots(taskerId);
      set({ slots: res.data, loading: false });
    } catch (error) {
      set({
        error: error.response?.data || "Failed to load slots",
        loading: false,
      });
    }
  },

  // Create a booking
  createBooking: async (taskerId, taskId, availabilitySlotId, description) => {
    set({ loading: true, error: null });

    const clientId = useBookingStore.getState().getClientId();
    
    console.log("Debug info:");
    console.log("Client ID:", clientId);
    console.log("Tasker ID:", taskerId);
    console.log("Task ID:", taskId);
    console.log("Availability Slot ID:", availabilitySlotId);
    console.log("Description:", description);

    if (!clientId) {
      set({ 
        error: "User not authenticated. Please log in again.", 
        loading: false 
      });
      return false;
    }

    const payload = {
      client: clientId,
      tasker: taskerId,
      task: taskId,
      availability_slot: availabilitySlotId,
      description: description,
    };

    console.log("📤 Sending booking payload:", payload);

    try {
      const res = await bookingService.createBooking(payload);

      if (res && res.data) {
        set((state) => ({
          bookings: [...state.bookings, res.data],
          loading: false,
        }));
        return true;
      } else {
        set({ error: "No booking data returned", loading: false });
        return false;
      }
    } catch (error) {
      set({
        error: error?.response?.data || "Failed to create booking",
        loading: false,
      });
      console.error("Booking request failed with payload:", payload);
      console.error("Error details:", error.response?.data || error.message);
      return false;
    }
  },
}));

export default useBookingStore;
