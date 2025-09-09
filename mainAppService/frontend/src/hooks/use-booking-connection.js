import { useEffect, useState } from "react";
import { useAuth } from "../store/AuthProvider";

export default function useBookingConnection() {
  const [ws, setWs] = useState(null);
  const [bookings, setBookings] = useState([]);
  const { userId } = useAuth();

  useEffect(() => {
    if (userId) {
      const websocket = new WebSocket("ws://localhost:5000/api/ws");

      websocket.onmessage = (event) => {
        const message = JSON.parse(event.data);

        switch (message?.type) {
          case "all_bookings":
            setBookings(message.data);
            break;

          case "new_booking":
            console.log("MESSAGE");
            console.log(message);

            console.log(bookings);

            setBookings((prev) =>
              prev.map((booking) =>
                booking.id === message.appointment_id
                  ? { ...booking, booked_by: message.booked_by }
                  : booking
              )
            );
            break;

          case "canceled_booking":
            setBookings((prev) =>
              prev.map((booking) =>
                booking.id === message.appointment_id
                  ? { ...booking, booked_by: undefined }
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

  const cancelAppointment = (appointment) => {
    if (ws)
      ws.send(
        JSON.stringify({
          type: "unbook",
          user_id: userId,
          appointment_id: appointment.id,
        })
      );
  };

  return { bookings, sendMessage, bookAppointment, cancelAppointment };
}
