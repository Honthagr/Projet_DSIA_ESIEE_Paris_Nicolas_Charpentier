import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/css/SecuriteManager.css"; // Import the CSS file

const API_BASE_URL = "http://localhost:8080";

function SecuriteManager({ token, onUpdate }) {
  const navigate = useNavigate();

  const handleSecurite = async () => {
    try {
      await axios.post(
        `${API_BASE_URL}/user/securite`,
        null,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      alert("Security settings updated successfully!");
      onUpdate();

    } catch (error) {
      console.error("Error updating security settings:", error);
      alert("Failed to update security settings. Please try again.");
    }
  };

  const handleDeleteAccount = async () => {
    const isConfirmed = window.confirm(
      "Are you sure you want to delete your account? This action cannot be undone."
    );

    if (isConfirmed) {
      try {
        console.log("Attempting to delete account...");
        await axios.delete(`${API_BASE_URL}/user/delete`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Account deleted successfully!");

        console.log("Clearing token...");
        localStorage.removeItem("token");

        console.log("Redirecting to login...");
        navigate("/login");

        setTimeout(() => {
          window.location.reload();
        }, 500);
      } catch (error) {
        console.error("Error deleting account:", error);
        alert("Failed to delete account. Please try again.");
      }
    } else {
      console.log("User canceled account deletion.");
    }
  };

  return (
    <div className="securite-manager">
      <h3 className="securite-title">Security and Account Management</h3>
      <button type="button" className="securite-button" onClick={handleSecurite}>
        Update Security Settings
      </button>
      <button
        className="securite-button delete-button"
        onClick={handleDeleteAccount}
      >
        Delete Account
      </button>
    </div>
  );
}

export default SecuriteManager;