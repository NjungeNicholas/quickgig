import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import useAuthStore from "../stores/authstore";

function Register() {
    const register = useAuthStore((state) => state.register);
    const error = useAuthStore((state) => state.error);
    const loading = useAuthStore((state) => state.loading);

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [password_confirm, setPasswordConfirm] = useState("");

    const navigate = useNavigate();

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
            navigate("/login");

        }
    };

    return (
        <div className="p-6 max-w-md mx-auto shadow-md mt-28">
            <h2 className="font-header text-2xl mb-4">Register</h2>
            <form className="space-y-4" onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={username}
                    onChange={handleChange}
                    className="p-3 rounded-lg border bg-gray-100 hover:bg-gray-200 w-full"
                />
                <br />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={email}
                    onChange={handleChange}
                    className="p-3 rounded-lg border bg-gray-100 hover:bg-gray-200 w-full"
                />
                <br />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={password}
                    onChange={handleChange}
                    className="p-3 rounded-lg border bg-gray-100 hover:bg-gray-200 w-full"
                />
                <br />
                <input
                    type="password"
                    name="password_confirm"
                    placeholder="Confirm Password"
                    value={password_confirm}
                    onChange={handleChange}
                    className="p-3 rounded-lg border bg-gray-100 hover:bg-gray-200 w-full"
                />
                <br />
                <button type="submit" disabled={loading} className="px-4 py-2 rounded bg-primary text-white hover:bg-blue-300 justify-center w-full">
                    {loading ? "Registering..." : "Register"}
                </button>
                <p className="text-center">
                    Already have an account? <Link to="/login" className="text-blue-500">Login</Link>
                </p>
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