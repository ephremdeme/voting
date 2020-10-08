import React, { Component } from "react";
import { BrowserRouter as Router } from "react-router-dom";
import Routes from "../src/components/Routes";
import TopNavigation from "./components/topNavigation";
import SideNavigation from "./components/sideNavigation";
import Footer from "./components/Footer";
import "./index.css";
import AppHeader from "./components/layout/AppHeader";

class App extends Component {
  render() {
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
  }
}

export default App;
