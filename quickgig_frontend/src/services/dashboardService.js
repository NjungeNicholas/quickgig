import { PRIVATE_URL } from "./api";

export const getClientTasks = () => {
    return PRIVATE_URL.get("tasks/bookings/client/");
};

export const getTaskerTasks = () => {
    return PRIVATE_URL.get("tasks/bookings/tasker/");
};
