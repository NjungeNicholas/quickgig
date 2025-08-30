import { PUBLIC_URL, PRIVATE_URL } from "./api";

export const register = ({email, username, password, password_confirm }) => {
    return PUBLIC_URL.post("accounts/auth/register/", { email, username, password, password_confirm });
};
export const login = ({ email, password }) => {
    return PUBLIC_URL.post("accounts/auth/login/", { email, password });
};
export const getUserProfile = () => {
    return PRIVATE_URL.get("accounts/auth/users/me/");
};