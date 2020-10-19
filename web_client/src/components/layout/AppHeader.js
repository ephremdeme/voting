import React, { useState } from "react";
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
import { useSelector, useDispatch } from "react-redux";
import { signOutUser } from "../auth/authSlices";

const AppHeader = () => {
  const [collapse, setCollapse] = useState(false);
  const dispatch = useDispatch();

  const { isAuthenticated, user } = useSelector((state) => state.auths);

  const onClick = () => {
    setCollapse({
      collapse: !collapse,
    });
  };

  const handleLogout=()=>{
    dispatch(signOutUser())
  }

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
      <MDBNavbarToggler onClick={onClick} />
      <MDBCollapse isOpen={collapse} navbar>
        <MDBNavbarNav right>
          {isAuthenticated && (
            <MDBNavItem className="mx-1">
              <MDBNavLink to="/admin">
                <MDBIcon className="fas fa-tachometer-alt" />
                Dashboard
              </MDBNavLink>
            </MDBNavItem>
          )}
          <MDBNavItem className="mx-1">
            <MDBNavLink to="/explore">
              <MDBIcon icon="fa-search" fab className="fas fa-search" />
              BlockChain Explore
            </MDBNavLink>
          </MDBNavItem>

          <MDBNavItem className="mx-1">
            <MDBNavLink to="/vote/create_vote">
              <MDBIcon fab icon="fa-plus" className="fas fa-plus" />
              Create Vote
            </MDBNavLink>
          </MDBNavItem>
        </MDBNavbarNav>

        <MDBNavbarNav right>
          {!isAuthenticated && (
            <React.Fragment>
              <MDBNavItem className="mx-1">
                <MDBNavLink to="/login">Login</MDBNavLink>
              </MDBNavItem>
              <MDBNavItem className="mx-1">
                <MDBNavLink to="/signup">Sign Up</MDBNavLink>
              </MDBNavItem>
            </React.Fragment>
          )}

          {isAuthenticated && (
            <React.Fragment>
              <MDBNavItem className="mx-1">
                <MDBNavLink to="#!">{user.name}</MDBNavLink>
              </MDBNavItem>
              <MDBNavItem className="mx-1">
                <MDBNavLink to="#!" onClick={ handleLogout}>Sign Out</MDBNavLink>
              </MDBNavItem>
            </React.Fragment>
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
};

export default AppHeader;
