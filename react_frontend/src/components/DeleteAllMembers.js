import React from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const API_BASE_URL = "http://localhost:8080";

function DeleteAllMembers({ token }) {
  const navigate = useNavigate();
  const handleDelete = async () => {
    const isConfirmed = window.confirm(
      "Are you sure you want to delete all members? This action cannot be undone."
    );

    if (isConfirmed) {
      try {
        await axios.delete(`${API_BASE_URL}/admin/delete_all_members`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("All members deleted successfully!");
        console.log("Clearing token...");
        localStorage.removeItem("token");

        console.log("Redirecting to login...");
        navigate("/login");

        setTimeout(() => {
          window.location.reload();
        }, 500);

      } catch (err) {
        console.error("Error deleting all members:", err);
        alert("Failed to delete all members. Please try again.");
      }
    }
  };

  return (
    <div>
      <h3>Delete All Members</h3>
      <button onClick={handleDelete} style={{ color: "red" }}>
        Delete All Members
      </button>
    </div>
  );
}

export default DeleteAllMembers;