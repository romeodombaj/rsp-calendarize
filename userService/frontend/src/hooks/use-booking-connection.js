import { useEffect, useState } from "react";

export default function useBookingConnection(userId = undefined) {
  const [ws, setWs] = useState(null);
  const [messages, setMessages] = useState(["MESSAGE ONE"]);
  const [input, setInput] = useState("");

  useEffect(() => {
    if (userId) {
      const websocket = new WebSocket("ws://localhost:5000/api/ws");

      websocket.onopen = () => console.log("WEBSOCKET Connected");

      websocket.onmessage = (event) => {
        setMessages((prev) => [...prev, JSON.parse(event.data)]);
      };
      
      setWs(websocket);

      return () => websocket.close();
    }
  }, [userId]);

  useEffect(() => {
    console.log(messages);
  }, [messages]);

  const sendMessage = (message) => {
    if (ws) ws.send(JSON.stringify({ id: userId, message }));
    //setMessages((prev) => [...prev, message]);
  };

  return { messages, sendMessage };
}
