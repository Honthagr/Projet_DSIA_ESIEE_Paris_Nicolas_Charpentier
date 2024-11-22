import axios from "axios";

const API_BASE_URL = "http://localhost:8080";

// Example: Login API call
export const login = async (email, password) => {
    const response = await axios.get(`${API_BASE_URL}/connection`, {
      params: { email, password },
    });
    return response.data;
  };

// User Balance
export const getUserBalance = async (token) => {
  const response = await axios.get(`${API_BASE_URL}/user/balance`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// User's IBAN
export const getUserIBAN = async (token) => {
  const response = await axios.get(`${API_BASE_URL}/user/IBAN`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// Obtain Historique
export const getUserHistorique = async (token) => {
  const response = await axios.get(`${API_BASE_URL}/user/historique`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// Do a expense
export const makeExpense = async (token, amount) => {
  const response = await axios.post(
    `${API_BASE_URL}/user/depense`,
    null, // Si el cuerpo está vacío
    {
      headers: { Authorization: `Bearer ${token}` },
      params: { Amount: amount }, // Send amount as query
    }
  );
  return response.data;
};

// Do a transfer
export const makeTransfer = async (token, transferiban, amount) => {
    const response = await axios.post(
      `${API_BASE_URL}/user/virement`,
      null, 
      {
        headers: { Authorization: `Bearer ${token}` },
        params: { IBAN_User2 : transferiban,
            Amount: amount }, //Send to iban and amount 
      }
    );
    return response.data;
  };