import React, { useState } from "react";
import axios from "axios";
import "../styles/css/AbonnementManager.css"; // Import the CSS file

const API_BASE_URL = "http://localhost:8080"; // Replace with your backend URL

function AbonnementManager({ token, onUpdate }) {
  const [abonnementData, setAbonnementData] = useState({
    IBAN_User2: "",
    Amount: "",
  });
  const [deleteAbonnementID, setDeleteAbonnementID] = useState("");

  const handleAddAbonnement = async (e) => {
    e.preventDefault();
    if (!abonnementData.IBAN_User2 || !abonnementData.Amount) {
      alert("Please provide both IBAN and Amount.");
      return;
    }
    try {
      await axios.post(
        `${API_BASE_URL}/user/abonnement`,
        null,
        {
          headers: { Authorization: `Bearer ${token}` },
          params: abonnementData,
        }
      );
      alert("Subscription added successfully!");
      setAbonnementData({ IBAN_User2: "", Amount: "" }); // Reset input fields
      onUpdate(); // Trigger parent refresh
    } catch (error) {
      console.error("Error adding abonnement:", error);
      alert("Failed to add abonnement. Please try again.");
    }
  };

  const handleDeleteAbonnement = async (e) => {
    e.preventDefault();
    if (!deleteAbonnementID) {
      alert("Please provide the subscription ID to delete.");
      return;
    }
    try {
      await axios.delete(`${API_BASE_URL}/user/delete_abonnement`, {
        headers: { Authorization: `Bearer ${token}` },
        params: { ID_Subscription: deleteAbonnementID },
      });
      alert("Subscription deleted successfully!");
      setDeleteAbonnementID(""); // Reset input field
      onUpdate(); // Trigger parent refresh
    } catch (error) {
      console.error("Error deleting Subscription:", error);
      alert("Failed to delete Subscription. Please try again.");
    }
  };

  return (
    <div className="abonnement-manager-container">
      <h3 className="abonnement-title">Manage Subscription</h3>

      {/* Add Abonnement Form */}
      <form className="abonnement-form" onSubmit={handleAddAbonnement}>
        <input
          className="abonnement-input"
          type="text"
          placeholder="IBAN User 2"
          value={abonnementData.IBAN_User2}
          onChange={(e) =>
            setAbonnementData({ ...abonnementData, IBAN_User2: e.target.value })
          }
        />
        <input
          className="abonnement-input"
          type="number"
          placeholder="Amount"
          value={abonnementData.Amount}
          onChange={(e) =>
            setAbonnementData({ ...abonnementData, Amount: e.target.value })
          }
        />
        <button className="abonnement-button" type="submit">
          Add Abonnement
        </button>
      </form>

      {/* Delete Abonnement Form */}
      <form className="abonnement-form" onSubmit={handleDeleteAbonnement}>
        <input
          className="abonnement-input"
          type="text"
          placeholder="Subscription ID to delete"
          value={deleteAbonnementID}
          onChange={(e) => setDeleteAbonnementID(e.target.value)}
        />
        <button className="abonnement-button delete" type="submit">
          Delete Abonnement
        </button>
      </form>
    </div>
  );
}

export default AbonnementManager;