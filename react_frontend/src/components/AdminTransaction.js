import React, { useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:8080";

function AdminTransaction({ token }) {
  const [iban, setIban] = useState("");
  const [amount, setAmount] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!iban || !amount) {
      alert("Please provide both IBAN and Amount.");
      return;
    }

    try {
      await axios.post(
        `${API_BASE_URL}/admin/admin_transaction`,
        null,
        {
          headers: { Authorization: `Bearer ${token}` },
          params: {
            IBAN_Member: iban,
            Amount: amount,
          },
        }
      );
      alert("Transaction completed successfully!");
      setIban("");
      setAmount("");
    } catch (err) {
      console.error("Error performing transaction:", err);
      alert("Failed to perform transaction. Please try again.");
    }
  };

  return (
    <div>
      <h3>Admin Transaction</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="IBAN Member"
          value={iban}
          onChange={(e) => setIban(e.target.value)}
        />
        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <button type="submit">Submit Transaction</button>
      </form>
    </div>
  );
}

export default AdminTransaction;