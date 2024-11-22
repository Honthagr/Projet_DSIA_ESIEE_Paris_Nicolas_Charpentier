import React from "react";
import "../styles/css/TransactionHistory.css"; // Import the CSS file

function TransactionHistory({ transactions }) {
  if (!transactions || transactions.length === 0) {
    return <p className="no-transaction">No transaction history available.</p>;
  }

  return (
    <div className="transaction-history-container">
      <h3 className="transaction-history-title">Transaction History</h3>
      <ul className="transaction-history-list">
        {transactions.map((transaction) => (
          <li key={transaction.id} className="transaction-item">
            {transaction.type === "Subscription" && (
              <span className="transaction-id">
                <strong>ID:</strong> {transaction.id} |{" "}
              </span>
            )}
            <span className="transaction-type">{transaction.type}:</span>{" "}
            <span className="transaction-value">${transaction.value}</span> -{" "}
            <span className="transaction-description">{transaction.description}</span>{" "}
            <span className="transaction-date">
              on {new Date(transaction.updated_at).toLocaleString()}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TransactionHistory;