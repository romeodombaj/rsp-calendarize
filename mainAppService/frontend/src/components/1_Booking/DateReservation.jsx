import { useAuth } from "../../store/AuthProvider";
import styles from "./DateReservation.module.css";

export default function DateReservation({
  selectedDate,
  bookings,
  bookAppointment,
}) {
  const { userId } = useAuth();

  console.log(userId)

  const filteredBookings =
    bookings?.filter((el) => {
      const bookingDate = new Date(el.date);
      const selDate = new Date(selectedDate);

      return (
        bookingDate.getFullYear() === selDate.getFullYear() &&
        bookingDate.getMonth() === selDate.getMonth() &&
        bookingDate.getDate() === selDate.getDate()
      );
    }) || [];

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.header}>
          {selectedDate &&
            new Date(selectedDate)?.toLocaleDateString("en-US", {
              day: "2-digit",
              month: "long",
              year: "numeric",
            })}
        </div>

        <div className={styles.list}>
          {(filteredBookings || []).map((el, i) => (
            <div
              key={i}
              className={`${styles.appointment} ${
                el.booked_by &&
                (el.booked_by === userId
                  ? styles[`current-booked`]
                  : styles[`other-booked`])
              }`}
              onClick={() => {
                bookAppointment(el);
              }}
            >
              <div className={styles[`appointment-book`]}>
                Book{" "}
                {new Date(el.date).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}{" "}
              </div>
              <div className={styles[`appointment-name`]}> {el.name}</div>
              <div className={styles[`appointment-date`]}>
                {new Date(el.date).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
