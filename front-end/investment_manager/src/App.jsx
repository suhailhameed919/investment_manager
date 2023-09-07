//need use effect that sends request requiring auth, if fails, you'll know you don't have token (in curriculum)



import React, { useState, useEffect } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';
import Navbar from "./components/Navbar";
import { Outlet } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { api } from "./utilities";


export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  // const [savedPredictions, setSavedPredictions] = useState([]);
  const navigate = useNavigate();
  const [user, setUser] = useState("");

  useEffect(() => {
    whoAmI();
  }, []);
  

  const whoAmI = async () => {
    let token = localStorage.getItem("token");
    if (token) {
      api.defaults.headers.common["Authorization"] = `Token ${token}`;
      let response = await api.get("users/info/");
      if (response.data.username) {
        setUser(response.data);
        navigate("/home");
        
      }
    } else {
      // If no token is found, navigate to the login page
      navigate("/login");
    }
  };







  
  const handleLogin = (username) => {
    setLoggedIn(true);
    setUsername(username);
    
  };

  const handleLogout = () => {
    setLoggedIn(false);
    setUsername("");
    setSavedPredictions([]); // Clearing saved predictions when log out
  };

  // const handleSavePrediction = (prediction) => {
  //   setSavedPredictions([...savedPredictions, prediction]);
  // };

  return (
    <>
      <Navbar loggedIn={loggedIn} username={username} onLogout={handleLogout} />
      <Outlet
        context={{
          loggedIn,
          username,
          // savedPredictions,
          handleLogin,
          // handleSavePrediction,
        }}
      />
    </>
  );
}


