import { useEffect, useState } from "react";

export default function useBookingConnection(userId = undefined) {
  const [ws, setWs] = useState(null);
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    if (userId) {
      const websocket = new WebSocket("ws://localhost:5000/api/ws");

      websocket.onmessage = (event) => {
        console.log("ON MESSAGE TRIGGERED");
        const message = JSON.parse(event.data);

        console.log("WEBSOCKER MESSAGE");
        console.log(message);

        if (message.type === "all_bookings") {
          setBookings(message.data);
        } else {
          setBookings((prev) => [...prev, message]);
        }
      };

      websocket.onopen = () => console.log("WEBSOCKET Connected");

      setWs(websocket);

      return () => websocket.close();
    }
  }, [userId]);

  useEffect(() => {
    console.log("bookings OUTPUT CHANGE");
    console.log(bookings);
  }, [bookings]);

  const sendMessage = (message) => {
    if (ws) ws.send(JSON.stringify({ id: userId, message }));
  };

  return { bookings, sendMessage };
}
