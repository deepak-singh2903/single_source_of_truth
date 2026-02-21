import Sidebar from "./Sidebar"

function Layout({ children }) {
  return (
    <div style={{ display: "flex" }}>
      <Sidebar />
      <div style={{ flex: 1, padding: "30px", backgroundColor: "#f3f4f6" }}>
        {children}
      </div>
    </div>
  )
}

export default Layout
