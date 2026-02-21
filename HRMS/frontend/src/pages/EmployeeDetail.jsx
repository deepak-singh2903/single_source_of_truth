import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"
import api from "../api/api"
import Layout from "../components/Layout"

function EmployeeDetail() {
  const { id } = useParams()
  const [employee, setEmployee] = useState(null)

  useEffect(() => {
    api.get(`http://127.0.0.1:5000/employees/${id}`)
      .then(res => setEmployee(res.data))
      .catch(err => console.error(err))
  }, [id])

  if (!employee) return <Layout>Loading...</Layout>

  return (
    <Layout>
      <h2>Employee Salary Preview</h2>

      <div style={{
        background: "white",
        padding: "20px",
        borderRadius: "10px",
        width: "400px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
      }}>
        <p><strong>Name:</strong> {employee.name}</p>
        <p><strong>Department:</strong> {employee.department}</p>
        <p><strong>Status:</strong> {employee.status}</p>
        <hr />
        <p><strong>Basic:</strong> ₹ {employee.basic}</p>
        <p><strong>HRA:</strong> ₹ {employee.hra}</p>
        <p><strong>PF:</strong> ₹ {employee.pf}</p>
        <hr />
        <p><strong>Gross:</strong> ₹ {employee.gross}</p>
        <p><strong>Net:</strong> ₹ {employee.net}</p>
      </div>
    </Layout>
  )
}

export default EmployeeDetail
