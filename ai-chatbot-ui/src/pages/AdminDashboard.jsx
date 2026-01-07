import { useEffect, useState } from "react";
import { fetchLeads, fetchLeadChats } from "../services/adminApi";
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer
} from "recharts";
import "../styles/admin.css";


const COLORS = ["#22c55e", "#facc15", "#ef4444"];



export default function AdminDashboard() {
  const [leads, setLeads] = useState([]);
  const [chats, setChats] = useState([]);
  const [selectedLead, setSelectedLead] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchLeads().then(res => setLeads(res.data));
  }, []);

  const openChats = async (lead) => {
    setSelectedLead(lead);
    const res = await fetchLeadChats(lead.id);
    setChats(res.data);
    setShowModal(true);
  };
  

  // ---------- Analytics ----------
  const statusData = ["hot", "warm", "cold"].map(status => ({
    name: status,
    value: leads.filter(l => l.status === status).length
  }));

  const intentData = Object.entries(
    leads.reduce((acc, l) => {
      acc[l.intent_level] = (acc[l.intent_level] || 0) + 1;
      return acc;
    }, {})
  ).map(([k, v]) => ({ name: k, value: v }));

  return (
    <div className="dashboard">

      {/* SUMMARY CARDS */}
      <div className="cards">
        <div className="card">
          <h3>Total Leads</h3>
          <p>{leads.length}</p>
        </div>
        <div className="card">
          <h3>Hot Leads</h3>
          <p>{statusData.find(s => s.name === "hot")?.value || 0}</p>
        </div>
        <div className="card">
          <h3>Warm Leads</h3>
          <p>{statusData.find(s => s.name === "warm")?.value || 0}</p>
        </div>
      </div>

      {/* CHARTS */}
      <div className="charts">
        <div className="chart-box">
          <h3>Lead Status</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={statusData} dataKey="value" innerRadius={60} outerRadius={90} animationDuration={800}>
                {statusData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-box">
          <h3>Intent Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={intentData} dataKey="value" outerRadius={90} animationDuration={800}>
                {intentData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* LEADS TABLE */}
      <div className="table-box">
        <h3>Leads</h3>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Score</th>
              <th>Status</th>
              <th>Intent</th>
            </tr>
          </thead>
          <tbody>
            {leads.map(l => (
              <tr key={l.id} onClick={() => openChats(l)}>
                <td>{l.id}</td>
                <td>{l.score}</td>
                <td className={`status-${l.status}`}>{l.status}</td>
                <td>{l.intent_level}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* CHAT PANEL */}
      {/* {selectedLead && (
        <div className="chat-panel">
            <h3>Chat History (Lead #{selectedLead.id})</h3>
            {chats.map((c, i) => (
            <div key={i} className="chat-message">
                <b>{c.sender}:</b> {c.message}
            </div>
            ))}
        </div>
        )} */}

        {showModal && selectedLead && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>

            <div className="modal-header">
                Chat History — Lead #{selectedLead.id}
                <button onClick={() => setShowModal(false)}>✕</button>
            </div>

            <div className="modal-body">
                {chats.map((c, i) => {
                const time = new Date(c.created_at).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit"
                });

                return (
                    <div key={i}>
                    <div
                        className={`chat-bubble ${
                        c.sender === "user" ? "chat-user" : "chat-bot"
                        }`}
                    >
                        {c.message}
                    </div>

                    <div
                        className={`chat-meta ${
                        c.sender === "user" ? "user" : "bot"
                        }`}
                    >
                        {c.sender} • {time}
                    </div>
                    </div>
                );
                })}
            </div>

            </div>
        </div>
        )}


    </div>
  );
}
