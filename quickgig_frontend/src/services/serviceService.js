// src/services/serviceService.js
import { PUBLIC_URL } from "./api";

// fetch all services
export const getServices = () => PUBLIC_URL.get("services/services");

// fetch taskers by service
export const getTaskersByService = (serviceId) =>
  PUBLIC_URL.get(`accounts/public/taskers/?skills=${serviceId}`);
