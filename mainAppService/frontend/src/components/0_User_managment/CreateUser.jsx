import { useState } from "react";
import styles from "./CreateUser.module.css";
import axios from "axios";
import { useNavigate } from "react-router";
import { useAuth } from "../../store/AuthProvider";

export default function CreateUser() {
  const navigate = useNavigate();
  const [name, setName] = useState();
  const [email, setEmail] = useState();
  const { setUserId } = useAuth();

  const onNameChange = (e) => {
    const value = e.target.value;
    setName(value);
  };

  const onEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
  };

  const onSubmit = async (e) => {
    e.preventDefault();

    if (!name || !email) return;

    const result = await axios.post(
      "http://localhost:5000/api/users/",
      {
        name: name,
        email: email,
      },
      {
        withCredentials: true,
      }
    );

    console.log("GETTING THE RESULTS");

    console.log(result);

    if (result?.status === 200) {
      setUserId(result.data.user_id);
      navigate("/");
    }
  };

  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={onSubmit}>
        <div className={styles.title}>User Info</div>
        <div className={styles[`input-group`]}>
          <label className={styles.label}>Name</label>
          <input
            className={styles.input}
            value={name}
            onChange={onNameChange}
          />
        </div>

        <div className={styles[`input-group`]}>
          <label className={styles.label}>Email</label>
          <input
            className={styles.input}
            type="email"
            value={email}
            onChange={onEmailChange}
          />
        </div>

        <button className={styles.button}>Submit</button>
      </form>
    </div>
  );
}
