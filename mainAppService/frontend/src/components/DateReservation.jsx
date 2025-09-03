import styles from "./DateReservation.module.css";

export default function DateReservation({ selectedDate }) {
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
      </div>
    </div>
  );
}
