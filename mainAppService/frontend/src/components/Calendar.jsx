import { useEffect } from "react";
import styles from "./Calendar.module.css";

export default function Caledar() {
  const getDaysInMonth = (year, month) => {
    const date = new Date(year, month, 1);
    const days = [];

    while (date.getMonth() === month) {
      days.push(new Date(date));
      date.setDate(date.getDate() + 1);
    }
    return days;
  };

  useEffect(() => {
    console.log("HERE");
    console.log(getDaysInMonth(2025, 7));
  }, []);

  return <div className={styles.contaienr}>CALENDAR</div>;
}
