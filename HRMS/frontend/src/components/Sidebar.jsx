import { Link } from "react-router-dom"

function Sidebar() {
  return (
    <div style={{
      width: "220px",
      height: "100vh",
      backgroundColor: "#1f2937",
      color: "white",
      padding: "20px",
      boxSizing: "border-box"
    }}>
      <h2 style={{ marginBottom: "30px" }}>HRMS</h2>

      <nav style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
        <Link to="/dashboard" style={linkStyle}>Dashboard</Link>
        <Link to="/employees" style={linkStyle}>Employees</Link>
        <Link to="/" style={linkStyle}>Logout</Link>
      </nav>
    </div>
  )
}

const linkStyle = {
  color: "white",
  textDecoration: "none",
  fontSize: "16px"
}

export default Sidebar
