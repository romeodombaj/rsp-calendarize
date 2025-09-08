import styles from "./DateReservation.module.css";

export default function DateReservation({ selectedDate, bookings }) {
  console.log(bookings);

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
          {bookings
            ?.filter((el) => {
              const bookingDate = new Date(el.date);
              const selDate = new Date(selectedDate);

              return (
                bookingDate.getFullYear() === selDate.getFullYear() &&
                bookingDate.getMonth() === selDate.getMonth() &&
                bookingDate.getDate() === selDate.getDate()
              );
            })
            ?.map((el, i) => (
              <div key={i} className={`${styles.appointment}`}>
                <div className={styles[`appointment-book`]}>
                  Book Appointment
                </div>
                {el.name}
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
