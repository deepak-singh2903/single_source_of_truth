import { useEffect, useState } from "react";
import api from "../api/api";
import Layout from "../components/Layout";
import { Link } from "react-router-dom";

function Employees() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("http://127.0.0.1:5000/employees")
      .then(res => {
        setEmployees(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching employees", err);
        setLoading(false);
      });
  }, []);

  return (
    <Layout>
      <h2>Employee List</h2>

      {loading ? (
        <p>Loading employees...</p>
      ) : employees.length === 0 ? (
        <p>No employees found.</p>
      ) : (
        <table
          border="1"
          cellPadding="8"
          style={{
            width: "100%",
            fontSize: "14px",
            borderCollapse: "collapse",
            marginTop: "20px"
          }}
        >
          <thead style={{ backgroundColor: "#f4f4f4" }}>
            <tr>
              <th>Emp Code</th>
              <th>Name</th>
              <th>Department</th>
              <th>Status</th>
              <th>PF Scheme</th>
              <th>Basic</th>
              <th>HRA Type</th>
              <th>Mode</th>
            </tr>
          </thead>
          <tbody>
            {employees.map(emp => (
              <tr key={emp.employee_id}>
                <td>{emp.employee_code}</td>
                <td>
                  <Link
                    to={`/employees/${emp.employee_id}`}
                    style={{ color: "#007bff", textDecoration: "none" }}
                  >
                    {emp.first_name} {emp.last_name}
                  </Link>
                </td>
                <td>{emp.department_name_snapshot}</td>
                <td>{emp.employment_status}</td>
                <td>{emp.pf_scheme_type}</td>
                <td>₹ {Number(emp.current_basic).toLocaleString()}</td>
                <td>{emp.hra_type}</td>
                <td>{emp.employment_mode}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Layout>
  );
}

export default Employees;
