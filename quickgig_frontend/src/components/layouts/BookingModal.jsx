import { useEffect, useState } from "react";
import useBookingStore from "../../stores/bookingStore";

export default function BookingModal({ tasker, task, taskData, onClose }) {
  const { slots, fetchTaskerSlots, createBooking, loading, error } = useBookingStore();
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (tasker) {
      fetchTaskerSlots(tasker.user.id);
    }
  }, [tasker, fetchTaskerSlots]);

  const handleSubmit = async () => {
    if (!selectedSlot || !description) {
      alert("Please select a time slot and add a description.");
      return;
    }
    
    const success = await createBooking(
      tasker.user.id,
      task, // This is the service ID
      selectedSlot,
      description
    );

    if (success) {
      alert("Booking confirmed!");
      onClose();
    }
  };

  if (!tasker) return null;

  return (
    <div className="fixed inset-0 bg-white bg-opacity-100 flex items-center justify-center">
      <div className="bg-white p-6 rounded-xl shadow-lg w-96">
        <h2 className="text-xl font-bold mb-4">
          Book {tasker.user.username}
        </h2>
        {taskData && (
          <p className="text-gray-600 mb-4">Service: {taskData.name}</p>
        )}

        <label className="block mb-2 font-semibold">Select Time Slot</label>
        <select
          className="w-full border p-2 rounded"
          value={selectedSlot || ""}
          onChange={(e) => setSelectedSlot(e.target.value)}
        >
          <option value="">-- Choose a slot --</option>
          {slots.map((slot) => (
            <option key={slot.id} value={slot.id}>
              {slot.date} | {slot.start_time} - {slot.end_time}
            </option>
          ))}
        </select>

        <label className="block mt-4 mb-2 font-semibold">Description</label>
        <textarea
          className="w-full border p-2 rounded"
          rows="3"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <div className="flex justify-end space-x-2 mt-4">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded bg-gray-300 hover:bg-gray-400"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="px-4 py-2 rounded bg-primary text-white hover:bg-blue-400"
          >
            {loading ? "Booking..." : "Confirm"}
          </button>
        </div>
        {/* Error Message */}
        {error && (
          <div style={{ color: "red" }}>
            {typeof error === "string"
              ? error
              : typeof error === "object"
                ? Object.entries(error).map(([key, value]) => (
                  <div key={key}>{key}: {Array.isArray(value) ? value.join(", ") : value}</div>
                ))
                : null}
          </div>)}
      </div>
    </div>
  );
}
