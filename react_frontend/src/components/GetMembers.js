import React, { useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:8080";

function GetMembers({ token }) {
  const [members, setMembers] = useState([]);
  const [error, setError] = useState("");

  const fetchMembers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/admin/members`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMembers(response.data); // Store members in state
      setError(""); // Clear any previous error
    } catch (err) {
      console.error("Error fetching members:", err);
      setError("Failed to fetch members. Please try again.");
    }
  };

  return (
    <div>
      <h3>Get Members</h3>
      <button onClick={fetchMembers}>Fetch Members</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {members.length > 0 && (
        <div>
          <h4>Members List</h4>
          <ul>
            {members.map((member) => (
              <li key={member.id}>
                <p>ID: {member.id}</p>
                <p>Name: {member.name} {member.family_name}</p>
                <p>Email: {member.email}</p>
                <p>IBAN: {member.IBAN}</p>
                <p>Balance: {member.money}</p>
                <p>Created At: {new Date(member.created_at).toLocaleString()}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default GetMembers;