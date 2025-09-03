import { cloneElement, useEffect, useState } from "react";
import styles from "./Calendar.module.css";
import { HiArrowCircleLeft } from "react-icons/hi";
import { HiArrowCircleRight } from "react-icons/hi";

const currentDate = new Date();

const daysInWeek = ["M", "T", "W", "T", "F", "S", "S"];

export default function Caledar({ selectedDate, setSelectedDate }) {
  const [selectedYear, setSelectedYear] = useState(currentDate.getFullYear());
  const [selectedMonth, setSelectedMonth] = useState(currentDate.getMonth());
  const [dates, setDates] = useState([]);

  const getDaysInMonth = (year, month) => {
    const date = new Date(year, month, 1);
    const days = [];

    const firstDayIndex = date.getDay();

    for (let i = 0; i < firstDayIndex; i++) {
      days.push(null);
    }

    while (date.getMonth() === month) {
      days.push(new Date(date));
      date.setDate(date.getDate() + 1);
    }

    return days;
  };

  const prevMonth = () => {
    if (selectedMonth === 0) {
      setSelectedYear((prev) => prev - 1);
      setSelectedMonth(11);
      return;
    }

    setSelectedMonth((prev) => prev - 1);
  };

  const nextMonth = () => {
    if (selectedMonth === 11) {
      setSelectedYear((prev) => prev + 1);
      setSelectedMonth(0);
      return;
    }

    setSelectedMonth((prev) => prev + 1);
  };

  const selectDate = (e) => {
    const value = e.currentTarget.getAttribute("date");

    if (!value) {
      return;
    }

    setSelectedDate(value);
  };

  useEffect(() => {
    setDates(getDaysInMonth(selectedYear, selectedMonth));
  }, [selectedYear, selectedMonth]);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles[`change-month-button`]} onClick={prevMonth}>
          <HiArrowCircleLeft />
        </div>

        <div className={styles[`month-name`]}>
          {new Date(selectedYear, selectedMonth)?.toLocaleDateString("en-US", {
            month: "long",
          })}
        </div>

        <div className={styles[`change-month-button`]} onClick={nextMonth}>
          <HiArrowCircleRight />
        </div>
      </div>
      <div className={styles[`date-grid`]}>
        {daysInWeek.map((day, i) => (
          <div className={styles[`day-container`]} key={i}>
            {day}
          </div>
        ))}

        {dates?.map((date, i) => {
          return (
            <div className={styles[`date-container`]} key={i}>
              <div
                className={`${styles.date} ${
                  new Date(date)?.getTime() ===
                    new Date(selectedDate)?.getTime() && styles[`date-selected`]
                }`}
                onClick={selectDate}
                date={date || undefined}
              >
                {date?.getDate()}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
