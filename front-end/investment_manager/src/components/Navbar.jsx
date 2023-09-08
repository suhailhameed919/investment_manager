import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { api } from "../utilities";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";

export default function CustomNavbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const logOut = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found");
        return;
      }

      const response = await api.post("users/logout/", null, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      if (response.status === 204) {
        localStorage.removeItem("token");
        delete api.defaults.headers.common["Authorization"];
        
        navigate("/login");
      }
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  const isLoginPage = location.pathname === "/login";
  const isSignupPage = location.pathname === "/signup";

  return (
    <>
      {!isLoginPage && !isSignupPage && (
        <Navbar bg="info" variant="light" expand="lg">
          <Container fluid>
            <Navbar.Brand as={Link} to="/home">
              Investment Manager
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                <Nav.Link as={Link} to="/home">
                  Home
                </Nav.Link>
              </Nav>
              <Button variant="outline-dark" onClick={logOut}>
                Logout
              </Button>
            </Navbar.Collapse>
          </Container>
        </Navbar>
      )}
    </>
  );
}
