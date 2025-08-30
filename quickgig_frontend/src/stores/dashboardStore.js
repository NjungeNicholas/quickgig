import { create } from 'zustand';
import { getClientTasks, getTaskerTasks } from '../services/dashboardService';

const useDashboardStore = create((set, get) => ({
    tasks: [],
    mode: "client", // "client" | "tasker"
    loading: false,
    error: null,

    setMode: (newMode) => {
        set({ mode: newMode });
        // Automatically fetch tasks when mode changes
        const { fetchTasks } = get();
        fetchTasks();
    },

    fetchTasks: async () => {
        set({ loading: true, error: null });
        try {
            const { mode } = get();
            let response;
            
            if (mode === "client") {
                response = await getClientTasks();
            } else {
                response = await getTaskerTasks();
            }
            
            set({ tasks: response.data, loading: false });
        } catch (error) {
            console.error("Failed to load tasks:", error.response?.data || error.message);
            set({ 
                error: error.response?.data || error.message || "Failed to load tasks",
                loading: false 
            });
        }
    },

    clearTasks: () => {
        set({ tasks: [], error: null });
    }
}));

export default useDashboardStore;
