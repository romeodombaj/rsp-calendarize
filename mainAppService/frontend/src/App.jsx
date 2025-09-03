import styles from "./App.module.css";
import { useState } from "react";
import Calendar from "./components/Calendar";
import DateReservation from "./components/DateReservation";

function App() {
  const [count, setCount] = useState(0);
  const [selectedDate, setSelectedDate] = useState();

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <Calendar
          selectedDate={selectedDate}
          setSelectedDate={setSelectedDate}
        />
        {selectedDate && <DateReservation selectedDate={selectedDate} />}
      </div>
    </div>
  );
}

export default App;
