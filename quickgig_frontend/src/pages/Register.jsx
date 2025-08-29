import { useState } from "react";
import useAuthStore from "../stores/authstore";

function Register() {
    const register = useAuthStore((state) => state.register);
    const error = useAuthStore((state) => state.error);
    const loading = useAuthStore((state) => state.loading);

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [password_confirm, setPasswordConfirm] = useState("");


    const handleChange = (e) => {
        const { name, value } = e.target;
        switch (name) {
            case "username":
                setUsername(value);
                break;
            case "email":
                setEmail(value);
                break;
            case "password":
                setPassword(value);
                break;
            case "password_confirm":
                setPasswordConfirm(value);
                break;
            default:
                break;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!email.includes("@")) {
            alert("Please enter a valid email");
            return;
        }
        if (password !== password_confirm) {
            alert("Passwords do not match");
            return;
        }
        const success = await register(email, username, password, password_confirm);
        if (success) {
            // Handle successful registration (e.g., redirect or show a success message)
            alert("Registration successful!");
        }
    };

    return (
        <div className="flex flex-col justify-center items-center m-5">
            <h2>Register</h2>
            <form className="flex flex-col justify-center p-3 border-secondary border-2 rad" onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={username}
                    onChange={handleChange}
                />
                <br />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={email}
                    onChange={handleChange}
                />
                <br />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={password}
                    onChange={handleChange}
                />
                <br />
                <input
                    type="password"
                    name="password_confirm"
                    placeholder="Confirm Password"
                    value={password_confirm}
                    onChange={handleChange}
                />
                <br />
                <button type="submit" disabled={loading}>
                    {loading ? "Registering..." : "Register"}
                </button>
            </form>
            {error && (
                <div style={{ color: "red" }}>
                    {typeof error === "string"
                        ? error
                        : typeof error === "object"
                            ? Object.entries(error).map(([key, value]) => (
                                <div key={key}>{key}: {Array.isArray(value) ? value.join(", ") : value}</div>
                              ))
                            : null}
                </div>
            )}
        </div>
    );
}

export default Register;