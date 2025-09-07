import { Route, Routes } from "react-router-dom";
import Booking from "./components/1_Booking/Booking";
import CreateUser from "./components/0_User_managment/CreateUser";
import styles from "./App.module.css";

function App() {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <Routes>
          <Route path="/" element={<Booking />} />
          <Route path="/create-user" element={<CreateUser />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
