import React, { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../utilities";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");


  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("users/signup/", { email, password });

      if (response.status === 201) {
        console.log("User registered successfully");
        setErrorMessage("registration successful, click login link below")
      } 
    } catch (error) {
      console.error("Error during registration:", error.response.data.message);
      setErrorMessage("user already exists");
    }
  };

  return (
    <div>
      <h2>Sign Up</h2>
      <form onSubmit={handleSignup}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div>
          <button type="submit">Sign Up</button>
        </div>
        {errorMessage && <p>{errorMessage}</p>}
      </form>
      <p>
        Already have an account?{" "}
        <Link to="/login">Login here</Link>
      </p>
    </div>
  );
}
