// src/store/serviceStore.js
import { create } from "zustand";
import { getServices, getTaskersByService }from "../services/serviceService";

const useServiceStore = create((set) => ({
  services: [],
  taskers: [],
  loading: false,
  error: null,

  fetchServices: async () => {
    set({ loading: true });
    try {
      const res = await getServices();
      set({ services: res.data, loading: false });
    } catch (error) {
      set({ loading: false, error: error.message || "Failed to load services" });
    }
  },

  fetchTaskers: async (serviceId) => {
    set({ loading: true });
    try {
      const res = await getTaskersByService(serviceId);
      set({ taskers: res.data, loading: false });
    } catch (error) {
      set({ loading: false, error: error.message || "Failed to load taskers" });
    }
  },
}));

export default useServiceStore;
