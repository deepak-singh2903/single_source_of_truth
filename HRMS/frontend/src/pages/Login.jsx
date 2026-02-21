import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Login() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!login || !password) {
      alert("Enter email/employee code and password");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/auth/login",
        {
          login: login,
          password: password,
        }
      );

      const { access_token, refresh_token } = response.data;

      // Store tokens
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);

      // Redirect to dashboard
      navigate("/dashboard");

    } catch (error) {
      alert("Invalid credentials");
      console.error(error);
    }
  };

  return (
    <div style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
      backgroundColor: "#f5f5f5"
    }}>
      <form
        onSubmit={handleLogin}
        style={{
          background: "white",
          padding: "40px",
          borderRadius: "10px",
          width: "300px",
          boxShadow: "0 4px 10px rgba(0,0,0,0.1)"
        }}
      >
        <h2 style={{ marginBottom: "20px" }}>HRMS Login</h2>

        <input
          type="text"
          placeholder="Email or Employee Code"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "15px"
          }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "20px"
          }}
        />

        <button
          type="submit"
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            cursor: "pointer"
          }}
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;
