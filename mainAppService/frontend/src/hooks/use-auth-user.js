import { useNavigate } from "react-router";
import { useAuth } from "../store/AuthProvider";
import { useState } from "react";
import axios from "axios";

const base_url = "/api/users/";

export default function useAuthUser() {
  const navigate = useNavigate();
  const { userId, setUserId } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const createUser = async ({ name, email }) => {
    if (!name || !email) return;

    setIsLoading(true);

    try {
      const result = await axios.post(
        base_url,
        {
          name: name,
          email: email,
        },
        {
          withCredentials: true,
        }
      );

      if (result?.status === 200) {
        setUserId(result.data.user_id);
        navigate("/");
      }
    } catch (err) {
      console.log("Could not Create user");
      console.log(err);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    createUser,
    isLoading,
  };
}
