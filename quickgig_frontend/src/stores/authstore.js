import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { register, login } from '../services/authService';

const useAuthStore = create(persist((set) => ({
    user: null,
    token : localStorage.getItem("token") || null,
    loading: false,
    error: null,

    register: async (email, username, password, password_confirm) => {
        set({ loading: true, error: null });
        try {
            const response = await register({ email, username, password, password_confirm });
            set({ user: response.data.user, token: response.data.access, loading: false });
            return true;
        } catch (error) {
            // Log the full error response for debugging
            console.log("Registration error:", error.response?.data);

            // Store the full error data, not just .detail
            set({
                loading: false,
                error: error.response?.data || error.message || "Registration failed"
            });
            return false;
        }
    },

    login: async (email, password) => {
        set({ loading: true, error: null });
        try {
            const response = await login({ email, password }); // <-- pass as object
            set({ user: response.data.user, token: response.data.access, loading: false });
            return true;
        } catch (error) {
            console.log("login error:", error.response?.data);
            set({ error: error.response?.data || error.message || "Login failed", loading: false });
            return false;
        }
    },

    logout: async () => {
        localStorage.removeItem("auth-storage-token");
        set({ user: null, token: null });
    },
}), {
    name: "auth-storage", // Name of the storage (must be unique)
    getStorage: () => localStorage, // Use localStorage as the storage
}));

export default useAuthStore;
