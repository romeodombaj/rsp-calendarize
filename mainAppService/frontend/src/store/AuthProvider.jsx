import React, { createContext, useContext, useEffect, useState } from "react";
import useAuthUser from "../hooks/use-auth-user";
import axios from "axios";

export const AuthContext = createContext({
  userId: null,
  setUserId: () => {},
});

export const useAuth = () => {
  return useContext(AuthContext);
};

const base_url = "http://localhost:5000/api/users/";

export const AuthProvider = ({ children }) => {
  const [userId, setUserId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const authenticateUser = async () => {
      try {
        const result = await axios.post(
          `${base_url}authenticate`,
          {},
          {
            withCredentials: true,
          }
        );

        if (result?.status === 200) {
          setUserId(result.data.user_id);
        }
      } catch (err) {
        console.log("Could not Authentica user");
      } finally {
        setIsLoading(false);
      }
    };

    authenticateUser();
  }, []);

  const authContext = {
    userId,
    setUserId,
    isLoading,
  };

  return (
    <AuthContext.Provider value={authContext}>{children}</AuthContext.Provider>
  );
};
