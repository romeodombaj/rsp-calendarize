import { useState } from "react";
import styles from "./CreateUser.module.css";
import axios from "axios";
import { useNavigate } from "react-router";
import { useAuth } from "../../store/AuthProvider";
import useAuthUser from "../../hooks/use-auth-user";

export default function CreateUser() {
  const [name, setName] = useState();
  const [email, setEmail] = useState();

  const { createUser } = useAuthUser();

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

    await createUser({ name, email });
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
