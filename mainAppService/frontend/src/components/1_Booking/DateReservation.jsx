import { useState } from "react";
import { useAuth } from "../../store/AuthProvider";
import styles from "./DateReservation.module.css";

export default function DateReservation({
  selectedDate,
  bookings,
  notifications,
  createNotification,
  cancelNotification,
  bookAppointment,
  cancelAppointment,
}) {
  const { userId } = useAuth();

  console.log(userId);

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
          {(filteredBookings || [])
            .sort((a, b) => new Date(a.date) - new Date(b.date))
            .map((el, i) => {
              const notification = notifications.find(
                (notification) => notification.booking_id === el.id
              );

              const [notificationCheckbox, setNotificationCheckbox] = useState(
                notification ? true : false
              );

              const onNotificationCheckboxChange = async (e, booking) => {
                const isChecked = e.target.checked;

                if (isChecked) {
                  await createNotification(booking);
                } else {
                  if (!notification) return;

                  await cancelNotification(notification);
                }

                setNotificationCheckbox(isChecked);
              };

              return (
                <div
                  key={i}
                  className={`${styles.appointment} ${
                    el.booked_by &&
                    (el.booked_by == userId
                      ? styles[`current-booked`]
                      : styles[`other-booked`])
                  }`}
                  onClick={() => {
                    !el.booked_by && bookAppointment(el);
                  }}
                >
                  <div className={styles[`appointment-name`]}> {el.name}</div>
                  <div className={styles[`appointment-date`]}>
                    {new Date(el.date).toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>

                  {el.booked_by === userId ? (
                    <div className={styles[`booked-actions`]}>
                      <label className={styles[`check-notification`]}>
                        <input
                          type="checkbox"
                          checked={notificationCheckbox}
                          onChange={(e) => onNotificationCheckboxChange(e, el)}
                        />
                        Send Reminder
                      </label>

                      <button
                        className={styles[`cancel-button`]}
                        onClick={() => cancelAppointment(el)}
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <div className={styles[`appointment-book`]}>
                      Book{" "}
                      {new Date(el.date).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}{" "}
                    </div>
                  )}
                </div>
              );
            })}
        </div>
      </div>
    </div>
  );
}
