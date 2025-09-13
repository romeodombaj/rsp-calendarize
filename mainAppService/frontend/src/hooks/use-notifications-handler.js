import { useNavigate } from "react-router";
import { useAuth } from "../store/AuthProvider";
import { useState } from "react";
import axios from "axios";

const base_url = "http://localhost:5000/api/notifications/";

export default function useNotificationsHandler() {
  const { userId } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [notifications, setNotifications] = useState([]);

  const createNotification = async (booking) => {
    if (!booking) return;

    setIsLoading(true);

    try {
      const result = await axios.post(base_url, {
        booking_id: booking.id,
        user_id: userId,
        booking_time: booking.date,
      });

      if (result?.status === 200) {
        setNotifications((prev) => [
          ...prev,
          {
            id: result.data.notification_id,
            booking_id: result.data.booking_id,
          },
        ]);
      }
    } catch (err) {
      console.log("Could not Create user");
      console.log(err);
    } finally {
      setIsLoading(false);
    }
  };

  const cancelNotification = async (notification) => {
    if (!notification) return;

    setIsLoading(true);

    try {
      const result = await axios.delete(`${base_url}${notification.id}`);

      if (result?.status === 200) {
        setNotifications((prev) =>
          prev.filter((el) => el.id !== notification.id)
        );
      }
    } catch (err) {
      console.log(err);
    }
  };

  return {
    notifications,
    setNotifications,
    cancelNotification,
    createNotification,
    isLoading,
  };
}
