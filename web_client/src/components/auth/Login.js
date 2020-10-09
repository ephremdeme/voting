import React from "react";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBBtn,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBLink,
} from "mdbreact";
import "../../index.css";
import { Link } from "react-router-dom";

const LogInPage = () => {
  return (
    <MDBContainer className="my-5 py-5">
      <MDBRow center>
        <MDBCol md="6">
          <MDBCard>
            <div className="header pt-3 unique-color-dark lighten-2">
              <MDBRow className="d-flex justify-content-start">
                <h3 className="text-white font-weight-normal mt-3 mb-4 pb-1 mx-5">Log In</h3>
              </MDBRow>
            </div>
            <MDBCardBody className="mx-4 mt-4">
              <MDBInput label="Your email" group type="text" validate />
              <MDBInput
                label="Your password"
                group
                type="password"
                validate
                containerClass="mb-0"
              />
              <p className="font-small grey-text d-flex justify-content-end">
                Forgot
                <a href="#!" className="dark-grey-text font-weight-bold ml-1">
                  Password?
                </a>
              </p>
              <div className="text-center mb-4 mt-5">
                <MDBBtn
                  rounded
                  color="unique-color-dark"
                  type="button"
                  className="btn-block text-white z-depth-2 unique-color-dark"
                >
                  Log in
                </MDBBtn>
              </div>
              <p className="font-small grey-text d-flex justify-content-center">
                Don't have an account?
                <Link
                  to="/signup"
                  className="dark-grey-text font-weight-bold ml-1"
                >
                  Sign up
                </Link>
              </p>
            </MDBCardBody>
          </MDBCard>
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
};

export default LogInPage;
