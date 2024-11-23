import React, { useState } from "react";
import axios from "axios";

const RegisterForm = ({ setIsLoginMode, setMessage }) => {
  const [formData, setFormData] = useState({
    national_id: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setMessage("Passwords do not match!");
      return;
    }

    try {
      await axios.post("http://127.0.0.1:8000/core/api/register/", {
        email: formData.email,
        national_id: formData.national_id,
        password: formData.password,
        confirm_password: formData.confirmPassword,
      });

      setMessage("Registration successful! You can now log in.");
      setIsLoginMode(true); // Switch to login mode
    } catch (error) {
      console.error("Error occurred during registration:", error);
      const errorMessage =
        error.response?.data?.email ||
        error.response?.data?.password ||
        "An error occurred. Please try again.";
      setMessage(errorMessage);
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          name="national_id"
          placeholder="National ID"
          value={formData.national_id}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default RegisterForm;
