import { useState } from "react";
import styles from "./CreateUser.module.css";

export default function CreateUser() {
  const [name, setName] = useState();
  const [email, setEmail] = useState();

  const onNameChange = (e) => {
    const value = e.target.value;
    setName(value);
  };

  const onEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
  };

  const onSubmit = (e) => {
    e.preventDefault();

    
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
