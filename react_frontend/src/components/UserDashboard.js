import React, { useEffect, useState } from "react";
import {
  getUserBalance,
  getUserIBAN,
  getUserHistorique,
  makeExpense,
  makeTransfer,
} from "../api";
import TransactionHistory from "./TransactionHistory";
import AbonnementManager from "./AbonnementManager";
import SecuriteManager from "./SecuriteManager";
import "../styles/css/UserDashboard.css";

function UserDashboard({ token }) {
  const [balance, setBalance] = useState(null);
  const [iban, setIban] = useState(null);
  const [history, setHistory] = useState([]);
  const [expenseAmount, setExpenseAmount] = useState("");
  const [transferIban, setTransferIban] = useState("");
  const [transferAmount, setTransferAmount] = useState("");

  const fetchData = async () => {
    try {
      const balanceData = await getUserBalance(token);
      setBalance(balanceData);

      const ibanData = await getUserIBAN(token);
      setIban(ibanData);

      const historyData = await getUserHistorique(token);
      const flattenedHistory = historyData.flat();
      setHistory(flattenedHistory);
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [token]);

  const handleExpenseSubmit = async (e) => {
    e.preventDefault();
    if (!expenseAmount || expenseAmount <= 0) {
      alert("Please enter a valid expense amount.");
      return;
    }
    try {
      await makeExpense(token, expenseAmount);
      alert("Expense recorded successfully!");
      setExpenseAmount("");
      fetchData();
    } catch (error) {
      console.error("Error making expense:", error);
      alert("Failed to record expense. Please try again.");
    }
  };

  const handleTransferSubmit = async (e) => {
    e.preventDefault();
    if (!transferAmount || transferAmount <= 0) {
      alert("Please enter a valid expense amount.");
      return;
    }
    try {
      await makeTransfer(token, transferIban, transferAmount);
      alert("Transfer recorded successfully!");
      setTransferAmount("");
      fetchData();
    } catch (error) {
      console.error("Error making transfer:", error);
      alert("Failed to record transfer. Please try again.");
    }
  };

  return (
    <div className="dashboard-container">
    {/* Balance and IBAN Section */}
    <div className="balance-iban dashboard-card">
      <div><strong>Balance:</strong> ${balance || "0"}</div>
      <div><strong>IBAN:</strong> {iban || "Unavailable"}</div>
    </div>
  
    <div className="dashboard-grid">
      {/* Manage Subscription */}
      <div className="dashboard-card">
        <div className="dashboard-card">
          <h3>Record a Transfer</h3>
            <form onSubmit={handleTransferSubmit}>
              <label htmlFor="transferAmount">Transfert Amount:</label>
              <input
                id="transferAmount"
                type="number"
                placeholder="Enter transfer amount"
                value={transferAmount}
                onChange={(e) => setTransferAmount(e.target.value)}
              />
              <input
                id="transferIBAN"
                type="string"
                placeholder="Enter User IBAN"
                value={transferIban}
                onChange={(e) => setTransferIban(e.target.value)}
              />
              <button type="submit">Submit Transfer</button>
            </form>
          </div>
        <AbonnementManager token={token} onUpdate={fetchData} />
      </div>
  
      {/* Security and Account Management */}
      <div className="dashboard-card">
        <div className="dashboard-card">
          <h3>Record an Expense</h3>
          <form onSubmit={handleExpenseSubmit}>
            <label htmlFor="expenseAmount">Expense Amount:</label>
            <input
              id="expenseAmount"
              type="number"
              placeholder="Enter expense amount"
              value={expenseAmount}
              onChange={(e) => setExpenseAmount(e.target.value)}
            />
            <button type="submit">Submit Expense</button>
          </form>
        </div>
        <SecuriteManager token={token} onUpdate={fetchData} />
      </div>
  
      {/* Transaction History */}
      <div className="dashboard-card transaction-history">
        <TransactionHistory transactions={history} />
      </div>
    </div>
  </div>
  );
}

export default UserDashboard;