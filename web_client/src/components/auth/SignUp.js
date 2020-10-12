import React, { useState } from "react";
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
import { useDispatch, useSelector } from "react-redux";
import { signUpUser } from "./authSlices";

const SignUpPage = (props) => {
  const dispatch = useDispatch();

  const [form, setForm] = useState({
    name: null,
    email: null,
    password: null,
  });

  const { isAuthenticated, loading, error } = useSelector(
    (state) => state.auths
  );

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm({
      ...form,
      [name]: value,
    });
  };

  const handleSubmit = () => {
    console.log(form);
    dispatch(signUpUser(form));
  };

  if (isAuthenticated) {
    props.history.push("/");
  }

  return (
    <MDBContainer className="my-5 py-5">
      <MDBRow center>
        <MDBCol md="6">
          <MDBCard>
            <div className="header pt-3 unique-color-dark lighten-2">
              <MDBRow className="d-flex justify-content-start">
                <h3 className="text-white font-weight-normal mt-3 mb-4 pb-1 mx-5">
                  Sign Up
                </h3>
              </MDBRow>
            </div>
            <MDBCardBody className="mx-4 mt-4">
              <MDBInput
                onChange={handleChange}
                name="name"
                label="Full Name"
                group
                type="text"
                validate
              />
              <MDBInput
                onChange={handleChange}
                name="email"
                label="Email"
                group
                type="text"
                validate
              />
              <MDBInput
                label=" Password"
                group
                onChange={handleChange}
                name="password"
                type="password"
                validate
                containerClass="mb-0"
              />

              <div className="text-center mb-4 mt-5">
                <MDBBtn
                  rounded
                  onClick={handleSubmit}
                  color="primary"
                  type="button"
                  className="btn-block text-white z-depth-2 unique-color-dark btn-block z-depth-2"
                >
                  Sign Up
                </MDBBtn>
              </div>
              <p className="font-small grey-text d-flex justify-content-center">
                Already have an account?
                <Link
                  to="login"
                  className="dark-grey-text font-weight-bold ml-1"
                >
                  Sign In
                </Link>
              </p>
            </MDBCardBody>
          </MDBCard>
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
};

export default SignUpPage;
