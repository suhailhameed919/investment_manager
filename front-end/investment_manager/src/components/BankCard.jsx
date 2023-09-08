import React from "react";
import { api } from "../utilities";

export default function PredictionCard({ prediction }) {
  // const { name, annual_income, monthlyExpenses, incomeIncrease, years, futureNetWorth } = prediction;
  const { prediction_name, state, filing_status, annual_income, avg_monthly_expenses, current_net_worth, future_net_worth, user_id } = bank;


  const handleDelete = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found");
        return;
      }

      const response = await api.delete(`predictions/deleteprediction/${prediction.id}/`, {
        headers: {
          "Authorization": `Token ${token}`
        }
      });

      if (response.status === 204) {
        console.log("prediction deleted")
        window.location.reload();

      }
    } catch (error) {
      console.error("Error deleting prediction:", error);
    }
  };






  return (
    <div className="prediction-card">
      <h3>Bank: {bank_name}</h3>
      <p>Current Balance: {bank_balance}</p> 
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}
