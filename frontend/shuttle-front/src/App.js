import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import AuthForm from "./Components/auth/AuthForm";
import EmailTemplateManager from "./Components/email/EmailTemplateManager";
import axios from "axios";

const App = () => {
  const [user, setUser] = useState(null); // Store user info
  const [isLoading, setIsLoading] = useState(true); // Loading state for user check

  // Fetch user data
  const fetchUser = async () => {
    const token = localStorage.getItem("authToken");
    if (token) {
      try {
        const response = await axios.get("http://127.0.0.1:8000/core/api/profile/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(response.data); // Assume response contains user info
      } catch (error) {
        console.error("Error fetching user:", error);
        setUser(null);
      }
    } else {
      setUser(null);
    }
    setIsLoading(false); // Stop loading
  };

  useEffect(() => {
    fetchUser();
  }, []);

  // ProtectedRoute Component
  const ProtectedRoute = ({ children }) => {
    if (isLoading) return <p>Loading...</p>;
    if (!user || !user.is_staff) return <Navigate to="/auth" />;
    return children;
  };

  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/auth">Authentication</Link>
            </li>
            {user?.is_staff && ( // Only show link if the user is a staff member
              <li>
                <Link to="/email-templates">Email Templates</Link>
              </li>
            )}
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<h1>Welcome to My App</h1>} />
          <Route path="/auth" element={<AuthForm onLogin={fetchUser} />} /> {/* Pass fetchUser as onLogin */}
          <Route
            path="/email-templates"
            element={
              <ProtectedRoute>
                <EmailTemplateManager />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
