import React, { createContext, useContext, useEffect, useState } from "react";

export const AuthContext = createContext({
  userId: null,
  setUserId: () => {},
});

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    console.log("user id changed: ", userId);
  }, [userId]);

  const authContext = {
    userId,
    setUserId,
  };

  return (
    <AuthContext.Provider value={authContext}>{children}</AuthContext.Provider>
  );
};
