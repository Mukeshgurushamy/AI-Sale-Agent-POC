import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const fetchLeads = () => {
  return axios.get(`${API_BASE}/admin/leads`);
};

export const fetchLeadChats = (leadId) => {
  return axios.get(`${API_BASE}/admin/leads/${leadId}/chats`);
};
