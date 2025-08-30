import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../stores/authstore";

function Login() {
    const login = useAuthStore((state) => state.login);
    const error = useAuthStore((state) => state.error);
    const loading = useAuthStore((state) => state.loading);

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const success = await login(email, password);
        if (success) {
            alert("successful login")
            navigate("/");
        }
    };

    return (
        <div className="p-6 max-w-md mx-auto shadow-md mt-28">
            <h2 className="font-header text-2xl mb-4 text-center">Login</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <input
                    type="email"
                    name="email"
                    value={email}
                    placeholder="joe@example.com"
                    onChange={(e) => setEmail(e.target.value)}
                    className="p-3 rounded-lg border bg-gray-100 hover:bg-gray-200 w-full"
                />
                <br /> 
                <input
                    type="password"
                    name="password"
                    placeholder="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="p-3 rounded-lg border bg-gray-100 hover:bg-gray-200 w-full"
                />
                <br />
                <button type="submit" disabled={loading} className="px-4 py-2 rounded bg-primary text-white hover:bg-blue-300 justify-center w-full">
                    {loading ? "login..." : "login"}
                </button>
                <p className="text-center">
                    Don't have an account? <Link to="/register" className="text-blue-500">Register</Link>
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
    )
}

export default Login