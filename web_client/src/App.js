import React, { Component } from "react";
import { BrowserRouter as Router } from "react-router-dom";
import Routes from "../src/components/Routes";
import TopNavigation from "./components/topNavigation";
import SideNavigation from "./components/sideNavigation";
import Footer from "./components/Footer";
import "./index.css";
import AppHeader from "./components/layout/AppHeader";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { fetchUsers } from "./components/auth/authSlices";

const App = () => {
  const dispach = useDispatch();
  const { isAuthenticated } = useSelector((state) => state.auths);
  useEffect(() => {
    dispach(fetchUsers());
  }, [isAuthenticated]);

  return (
    <Router>
      <div className="flexible-content">
        <AppHeader />

        <main>
          <Routes />
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
