import { useState } from "react";
import NeuralHero from "../components/NeuralHero";
import ChatWidget from "../components/ChatWidget";

export default function ChatPage() {
  const [chatOpen, setChatOpen] = useState(false);
  const [pulseId, setPulseId] = useState(0);

  return (
    <>
      <NeuralHero hidden={chatOpen} pulseId={pulseId} />

      <ChatWidget
        onOpen={() => setChatOpen(true)}
        onClose={() => setChatOpen(false)}
        onBotReply={() => {
          setPulseId(id => id + 1); // 🔥 GUARANTEED TRIGGER
        }}
      />
    </>
  );
}
