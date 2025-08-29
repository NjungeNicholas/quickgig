import { useState } from "react";
import { useNavigate } from "react-router-dom";
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
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    name="email"
                    value={email}
                    placeholder="joe@example.com"
                    onChange={(e) => setEmail(e.target.value)}
                />
                <br /> 
                <input
                    type="password"
                    name="password"
                    placeholder="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <br />
                <button type="submit" disabled={loading}>
                    {loading ? "login..." : "login"}
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
    )
}

export default Login