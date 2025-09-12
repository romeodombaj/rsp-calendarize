import styles from "./Booking.module.css";
import { useState } from "react";
import Calendar from "./Calendar";
import DateReservation from "./DateReservation";
import useBookingConnection from "../../hooks/use-booking-connection";
import useNotificationsHandler from "../../hooks/use-notifications-handler";

const userID = crypto.randomUUID();

function Booking() {
  const [count, setCount] = useState(0);
  const [selectedDate, setSelectedDate] = useState();
  const {
    notifications,
    setNotifications,
    createNotification,
    cancelNotification,
  } = useNotificationsHandler();

  const { bookings, setBookings, bookAppointment, cancelAppointment } =
    useBookingConnection({ notifications, setNotifications });

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <Calendar
          selectedDate={selectedDate}
          setSelectedDate={setSelectedDate}
        />
        {selectedDate && (
          <DateReservation
            selectedDate={selectedDate}
            bookings={bookings}
            notifications={notifications}
            createNotification={createNotification}
            cancelNotification={cancelNotification}
            bookAppointment={bookAppointment}
            cancelAppointment={cancelAppointment}
            userId={userID}
          />
        )}
      </div>
    </div>
  );
}

export default Booking;
