import React from "react";
import GetMembers from "./GetMembers";
import DeleteAllMembers from "./DeleteAllMembers";
import AdminTransaction from "./AdminTransaction";

function AdminDashboard({ token }) {
  return (
    <div>
      <h2>Admin Dashboard</h2>
      <p>Welcome Admin! Your token is: {token}</p>
      
      <GetMembers token={token} />
      <DeleteAllMembers token={token} />
      <AdminTransaction token={token} />
    </div>
  );
}

export default AdminDashboard;