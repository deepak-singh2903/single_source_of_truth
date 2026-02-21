import { useEffect, useState } from "react";
import api from "../api/axios";
import Layout from "../components/Layout";
import { Link, useNavigate } from "react-router-dom";

function Dashboard() {
  const [status, setStatus] = useState("Checking system status...");
  const navigate = useNavigate();

  useEffect(() => {
    const checkStatus = async () => {
      try {
        await api.get("/");
        setStatus("System Online");
      } catch (error) {
        setStatus("System Offline");

        // If unauthorized, force logout
        if (error.response?.status === 401) {
          handleLogout();
        }
      }
    };

    checkStatus();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/");
  };

  return (
    <Layout>
      <h2>HRMS Dashboard</h2>

      {/* Logout Button */}
      <button
        onClick={handleLogout}
        style={{
          marginTop: "10px",
          padding: "8px 16px",
          backgroundColor: "red",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer"
        }}
      >
        Logout
      </button>

      {/* System Status Card */}
      <div
        style={{
          marginTop: "20px",
          padding: "20px",
          backgroundColor: "white",
          borderRadius: "8px",
          width: "350px",
          boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
        }}
      >
        <h3>System Status</h3>
        <p
          style={{
            color: status === "System Online" ? "green" : "red",
            fontWeight: "bold"
          }}
        >
          {status}
        </p>
      </div>

      {/* Navigation Section */}
      <div
        style={{
          marginTop: "30px",
          display: "flex",
          gap: "20px"
        }}
      >
        <Link to="/employees">
          <button
            style={{
              padding: "10px 20px",
              backgroundColor: "#1976d2",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer"
            }}
          >
            View Employees
          </button>
        </Link>
      </div>
    </Layout>
  );
}

export default Dashboard;
