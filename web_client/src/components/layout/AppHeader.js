import React, { Component } from "react";
import {
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarNav,
  MDBNavbarToggler,
  MDBCollapse,
  MDBNavItem,
  MDBNavLink,
  MDBIcon,
} from "mdbreact";

class AppHeader extends Component {
  state = {
    collapse: false,
    isLoggenIn: false,
  };

  onClick = () => {
    this.setState({
      collapse: !this.state.collapse,
    });
  };

  toggle = () => {
    this.setState({
      dropdownOpen: !this.state.dropdownOpen,
    });
  };

  render() {
    const { isLoggenIn, collapse } = this.state;
    return (
      <MDBNavbar
        className="flexible-navbar"
        color="unique-color-dark"
        dark
        expand="md"
        scrolling
      >
        <MDBNavbarBrand href="/">
          <strong style={{ color: "whitesmoke" }}>ASTU VOTING</strong>
        </MDBNavbarBrand>
        <MDBNavbarToggler onClick={this.onClick} />
        <MDBCollapse isOpen={collapse} navbar>
          <MDBNavbarNav right>
            <MDBNavItem className="mx-1">
              <MDBNavLink to="/explore">
                <MDBIcon className="fas fa-search" />
                BlockChain Explore
              </MDBNavLink>
            </MDBNavItem>
            <MDBNavItem className="mx-1">
              <MDBNavLink to="#">
                <MDBIcon className="fas fa-plus" />
                Create Vote
              </MDBNavLink>
            </MDBNavItem>
          </MDBNavbarNav>

          <MDBNavbarNav right>
            {!isLoggenIn && (
              <React.Fragment>
                <MDBNavItem className="mx-1">
                  <MDBNavLink to="/login">Login</MDBNavLink>
                </MDBNavItem>
                <MDBNavItem className="mx-1">
                  <MDBNavLink to="/signup">Sign Up</MDBNavLink>
                </MDBNavItem>
              </React.Fragment>
            )}

            {isLoggenIn && (
              <MDBNavItem className="mx-1">
                <MDBNavLink to="#!">Sign Out</MDBNavLink>
              </MDBNavItem>
            )}

            <MDBNavItem>
              <a
                className="border border-light rounded mr-1 nav-link Ripple-parent"
                rel="noopener noreferrer"
                href="https://github.com/ephremdeme/voting"
                target="_blank"
              >
                <MDBIcon fab icon="github" className="mr-2" />
                Github
              </a>
            </MDBNavItem>
          </MDBNavbarNav>
        </MDBCollapse>
      </MDBNavbar>
    );
  }
}

export default AppHeader;
