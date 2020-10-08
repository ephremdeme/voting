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
    return (
      <MDBNavbar
        className="flexible-navbar"
        color="unique-color-dark"
        dark
        expand="md"
        scrolling
      >
        <MDBNavbarBrand href="/" >
          <strong style={{color: "whitesmoke"}}>ASTU VOTING</strong>
        </MDBNavbarBrand>
        <MDBNavbarToggler onClick={this.onClick} />
        <MDBCollapse isOpen={this.state.collapse} navbar>
          <MDBNavbarNav right>
            <MDBNavItem active>
              <MDBNavLink to="#">Home</MDBNavLink>
            </MDBNavItem>
            <MDBNavItem className="mx-1">
              <MDBNavLink to="#">  <icon className="fas fa-link" />BlockChain</MDBNavLink>
            </MDBNavItem>
            <MDBNavItem className="mx-1">
              <MDBNavLink to="#">
                <icon className="fas fa-plus" />
                Create Vote
              </MDBNavLink>
            </MDBNavItem>

            <MDBNavItem>
              <a
                className="border border-light rounded mr-1 nav-link Ripple-parent"
                rel="noopener noreferrer"
                href="https://github.com/mdbootstrap/React-Bootstrap-with-Material-Design"
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
