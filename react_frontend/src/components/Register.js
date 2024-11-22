import React, { useState } from "react";
import axios from "axios";
import "../styles/css/Register.css"; // Import CSS file

function Register() {
  const [formData, setFormData] = useState({
    name: "",
    family_name: "",
    email: "",
    password: "",
    password_admin: "",
  });
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const params = formData.password_admin? { password_admin: formData.password_admin }: {};
      await axios.post(
        "http://localhost:8080/nouveau_user",
        {
          name: formData.name,
          family_name: formData.family_name,
          email: formData.email,
          password: formData.password,
        },
        {
          params,
        }
      );
      setSuccess("User created successfully!");
      setFormData({ name: "", family_name: "", email: "", password: "", password_admin: "" });
    } catch (err) {
      setError("Failed to create user. Please try again.");
      console.error(err);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2 className="register-title">Register</h2>
        <form onSubmit={handleSubmit}>
          <div className="name-row">
            <input
              type="text"
              name="name"
              className="register-input half-width"
              placeholder="First Name"
              value={formData.name}
              onChange={handleChange}
            />
            <input
              type="text"
              name="family_name"
              className="register-input half-width"
              placeholder="Last Name"
              value={formData.family_name}
              onChange={handleChange}
            />
          </div>
          <input
            type="email"
            name="email"
            className="register-input"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
          />
          <input
            type="password"
            name="password"
            className="register-input"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
          />
          <input
            type="number"
            name="password_admin"
            className="register-input"
            placeholder="Admin Password (Optional)"
            value={formData.password_admin}
            onChange={handleChange}
          />
          <button type="submit" className="register-button">Register</button>
        </form>
        {success && <p className="success-message">{success}</p>}
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
}

export default Register;