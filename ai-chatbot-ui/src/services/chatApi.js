import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const startChat = () => {
  return axios.post(`${API_BASE}/chat/start`);
};

export const sendMessage = (leadId, message) => {
  return axios.post(`${API_BASE}/chat/message`, {
    lead_id: leadId,
    message
  });
};
