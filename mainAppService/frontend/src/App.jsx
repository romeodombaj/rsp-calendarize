import { Navigate, Outlet, Route, Routes } from "react-router-dom";
import Booking from "./components/1_Booking/Booking";
import CreateUser from "./components/0_User_managment/CreateUser";
import styles from "./App.module.css";
import { useAuth } from "./store/AuthProvider";
import axios from "axios";
import useAuthUser from "./hooks/use-auth-user";
import { useEffect } from "react";

function ProtectedRoute() {
  const { userId } = useAuth();
  const { authenticateUser } = useAuthUser();

  console.log("USER ID IN PROTECTION: ", userId);

  useEffect(() => {
    const checkAuth = async () => {
      await authenticateUser();
    };

    if (!userId) checkAuth();
  }, [authenticateUser]);

  console.log("HERE");

  // for testing
  //return <Outlet />;

  return userId ? <Outlet /> : <Navigate to="/create-user" />;
}

function App() {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <Routes>
          <Route path="/create-user" element={<CreateUser />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<Booking />} />
          </Route>

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
