import { PRIVATE_URL } from "./api";

export const createBooking = (data) => {
    return PRIVATE_URL.post("tasks/bookings/", data);
}

export const getTaskerSlots = (taskerId) => {
    return PRIVATE_URL.get(`tasks/slots/?tasker=${taskerId}`);
}