import styles from "./App.module.css";
import { useState } from "react";
import Calendar from "./components/Calendar";
import DateReservation from "./components/DateReservation";
import useBookingConnection from "./hooks/use-booking-connection";

const userID = crypto.randomUUID();

function App() {
  const [count, setCount] = useState(0);
  const [selectedDate, setSelectedDate] = useState();
  const { messages, sendMessage } = useBookingConnection(userID);

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
            messages={messages}
            sendMessage={sendMessage}
            userId={userID}
          />
        )}
      </div>
    </div>
  );
}

export default App;
