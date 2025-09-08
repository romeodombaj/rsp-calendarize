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

        switch (message?.type) {
          case "all_bookings":
            setBookings(message.data);
            break;

          case "new_booking":
            setBookings((prev) =>
              prev.map((booking) =>
                booking.id === message.appointment_id
                  ? { ...booking, booked_by: message.user_id }
                  : booking
              )
            );
            break;
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

  const bookAppointment = (appointment) => {
    if (ws)
      ws.send(
        JSON.stringify({
          type: "book",
          user_id: userId,
          appointment_id: appointment.id,
        })
      );
  };

  return { bookings, sendMessage, bookAppointment };
}
