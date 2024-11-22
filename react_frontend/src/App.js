import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import UserDashboard from "./components/UserDashboard";
import AdminDashboard from "./components/AdminDashboard";
import "./styles/css/App.css";

function App() {
  const [token, setToken] = useState(() => localStorage.getItem("token")); // Load token from localStorage

  const handleLogin = (token) => {
    setToken(token); // Save the token in the state
    localStorage.setItem("token", token); // Persist the token in localStorage
  };

  const handleLogout = () => {
  const isConfirmed = window.confirm(
    "Are you sure you want to log out?"
  );

  if (isConfirmed) {
    setToken(null); // Remove the token from the state
    
    localStorage.removeItem("token"); // Remove the token from localStorage
     }
};

  return (
    <div className="app-container">
      <Router>
        {/* Header */}
        <header className="app-header">
          <h1>Crédit ESIEE</h1>
        </header>

        {/* Navbar */}
        <nav className="navbar">
          {!token ? (
            <>
              <Link className="navbar-link" to="/login">
                Login
              </Link>
              <Link className="navbar-link" to="/register">
                Register
              </Link>
            </>
          ) : (
            <>
              <Link className="navbar-link" to="/user">
                User Dashboard
              </Link>
              <Link className="navbar-link" to="/admin">
                Admin Dashboard
              </Link>
              <button className="navbar-logout" onClick={handleLogout}>
                Logout
              </button>
            </>
          )}
        </nav>

        {/* Main Content */}
        <div className="main-content">
          <Routes>
            {/* Login Route */}
            <Route
              path="/login"
              element={token ? <Navigate to="/user" /> : <Login onLogin={handleLogin} />}
            />

            {/* Register Route */}
            <Route
              path="/register"
              element={token ? <Navigate to="/user" /> : <Register />}
            />

            {/* User Dashboard Route */}
            <Route
              path="/user"
              element={token ? <UserDashboard token={token} /> : <Navigate to="/login" />}
            />

            {/* Admin Dashboard Route */}
            <Route
              path="/admin"
              element={token ? <AdminDashboard token={token} /> : <Navigate to="/login" />}
            />

            {/* Route to handle pages not found */}
            <Route path="*" element={token ? <Navigate to="/user" /> : <Register />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;