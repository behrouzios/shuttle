import React, { useState, useEffect } from "react";
import LogInForm from "./LoginForm";
import RegisterForm from "./RegisterForm";
import UploadFile from "../Upload/UploadFile";
import EmailTemplateManager from "../email/EmailTemplateManager";
import "./AuthForm.css";

const AuthForm = () => {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [message, setMessage] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    if (token) {
      fetchUserData(token);
    }
  }, []);

  const fetchUserData = async (token) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/core/api/profile/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setUserData(data);
        setIsLoggedIn(true);
      } else {
        setIsLoggedIn(false);
        setUserData(null);
        localStorage.removeItem("authToken");
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
      setIsLoggedIn(false);
      setUserData(null);
      localStorage.removeItem("authToken");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    setIsLoggedIn(false);
    setUserData(null);
    setMessage("You have been logged out.");
  };

  if (isLoggedIn && userData) {
    return (
      <div className="container">
        <h1>Welcome to My App</h1>
        <h2>Hello, {userData.first_name || "User"}!</h2>
        <button onClick={handleLogout}>Logout</button>
        <div className="upload-section">
          <UploadFile setMessage={setMessage} />
        </div>
        {userData.is_staff && (
          <div className="staff-section">
            <h3>Staff Section</h3>
            <EmailTemplateManager />
          </div>
        )}
        <p className={`message ${message.includes("success") ? "success" : "error"}`}>
          {message}
        </p>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Welcome to My App</h1>
      {isLoginMode ? (
        <LogInForm
          setIsLoggedIn={setIsLoggedIn}
          setMessage={setMessage}
          onLoginSuccess={fetchUserData}
        />
      ) : (
        <RegisterForm setIsLoginMode={setIsLoginMode} setMessage={setMessage} />
      )}
      <p className={`message ${message.includes("success") ? "success" : "error"}`}>
        {message}
      </p>
      <button onClick={() => setIsLoginMode(!isLoginMode)}>
        {isLoginMode ? "Switch to Register" : "Switch to Login"}
      </button>
    </div>
  );
};

export default AuthForm;
