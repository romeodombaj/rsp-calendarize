import styles from "./DateReservation.module.css";

export default function DateReservation({
  selectedDate,
  messages,
  sendMessage,
  userId,
}) {
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
          {messages?.map((el, i) => (
            <div key={i} className={`${el.id === userId && styles.highlight}`}>
              {el.message}
            </div>
          ))}
          <div onClick={() => sendMessage("New message")}>ADD MESSAGE</div>
        </div>
      </div>
    </div>
  );
}
