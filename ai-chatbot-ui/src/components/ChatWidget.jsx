import { useEffect, useRef, useState } from "react";
import axios from "axios";
import "../styles/chat.css";

const API_BASE = "http://127.0.0.1:8000";

const QUICK_REPLIES = [
  "Pricing details",
  "Book a demo",
  "Customer support"
];

export default function ChatWidget({ onOpen, onClose, onBotReply }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  const messagesEndRef = useRef(null);
  const sessionIdRef = useRef(null);

  /* =========================
     AUTO SCROLL
  ========================= */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  /* =========================
     START CHAT (ONCE)
  ========================= */
  useEffect(() => {
    const startChat = async () => {
      try {
        const res = await axios.post(`${API_BASE}/chat/start`);
        sessionIdRef.current = res.data.lead_id;

        setMessages([
          {
            sender: "bot",
            message: "Hi! How can I help you today?"
          }
        ]);
      } catch (err) {
        console.error("Chat start failed", err);
      }
    };

    startChat();
  }, []);

  /* =========================
     SEND MESSAGE
  ========================= */
  const sendMessage = async (text) => {
    if (!text.trim() || loading) return;

    setMessages(prev => [
      ...prev,
      { sender: "user", message: text }
    ]);

    setInput("");
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/chat/message`, {
        lead_id: sessionIdRef.current,
        message: text
      });

      // Natural delay for UX
      setTimeout(() => {
        setMessages(prev => [
          ...prev,
          { sender: "bot", message: res.data.reply }
        ]);

        setLoading(false);
        onBotReply?.(); // 🔥 TRIGGER NEURAL PULSE
      }, 600);

    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          sender: "bot",
          message: "Something went wrong. Please try again."
        }
      ]);
      setLoading(false);
    }
  };

  /* =========================
     RENDER
  ========================= */
  return (
    <>
      {/* FLOATING LAUNCHER */}
      <div
        className="chat-launcher"
        onClick={() => {
          setOpen(!open);
          onOpen?.();
        }}
        title="Chat with AI"
      >
        💬
      </div>

      {/* CHAT WINDOW */}
      {open && (
        <div className="chat-wrapper">
          <div className="chat-card">

            {/* HEADER */}
            <div className="chat-header">
              AI Sales Assistant
              <span
                className="chat-close"
                onClick={() => {
                  setOpen(false);
                  onClose?.();
                }}
              >
                ✕
              </span>
            </div>


            {/* MESSAGES */}
            <div className="chat-messages">
              {messages.map((m, i) => (
                <div
                  key={i}
                  className={`message ${m.sender}`}
                >
                  {m.message}
                </div>
              ))}

              {/* QUICK REPLIES (ONLY AT START) */}
              {messages.length <= 1 && (
                <div className="quick-replies">
                  {QUICK_REPLIES.map((q, i) => (
                    <div
                      key={i}
                      className="quick-reply"
                      onClick={() => sendMessage(q)}
                    >
                      {q}
                    </div>
                  ))}
                </div>
              )}

              {/* TYPING INDICATOR */}
              {loading && (
                <div className="message bot">
                  <div className="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* INPUT */}
            <div className="chat-input">
              <input
                type="text"
                placeholder="Type your message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") sendMessage(input);
                }}
              />
              <button onClick={() => sendMessage(input)}>
                Send
              </button>
            </div>

          </div>
        </div>
      )}
    </>
  );
}
