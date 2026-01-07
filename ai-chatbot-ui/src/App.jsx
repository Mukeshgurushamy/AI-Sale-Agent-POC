import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import AdminDashboard from "./pages/AdminDashboard";

function App() {
  return (
    <BrowserRouter>
      {/* Simple top navigation (optional but useful) */}
      <nav style={{ padding: "10px 20px", borderBottom: "1px solid #444", width: "100%" }}>
        <Link to="/" style={{ marginRight: 15 }}>
          Chatbot
        </Link>
        <Link to="/admin">
          Admin Dashboard
        </Link>
      </nav>

      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
