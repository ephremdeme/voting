import React from "react";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBProgress,
} from "mdbreact";

import "./result.css";
import { MobileOrTablet, Default, Desktop } from "../../../helper";

const AppResult = () => {
  return (
    <MDBContainer fluid className="py-2">
      <div className="my-3">
        <h1 className="title text-center mb-3">ASTU</h1>
        <MobileOrTablet>
          <h3 className=" title text-center">Results</h3>
          <CandidateResult />
          <CandidateResult />
          <CandidateResult />

          <VoteInfo />
        </MobileOrTablet>

        <Desktop>
          <MDBCardBody>
            <MDBRow>
              <MDBCol className="vl">
                <MDBRow className=" my-4">
                  <MDBCol>
                    <h3 className=" title">Results</h3>
                  </MDBCol>
                </MDBRow>
                <CandidateResult />
                <CandidateResult />
                <CandidateResult />
              </MDBCol>

              <MDBCol>
                <VoteInfo />
              </MDBCol>
            </MDBRow>
          </MDBCardBody>
        </Desktop>
      </div>
    </MDBContainer>
  );
};

const VoteInfo = () => {
  return (
    <React.Fragment>
      <MDBRow center className="ml-3 my-4">
        <MDBCol className="justify-content-center">
          <h3 className=" title text-center">Voting Link</h3>
        </MDBCol>
      </MDBRow>
      <MDBRow center className="my-4">
        <MDBCol className=" overflow-auto justify-content-center">
          <MobileOrTablet>
            <div className="my-2 vote-link text-center">
              http:localhost:3000/3jhjgdhsvdb
            </div>
          </MobileOrTablet>
          <Desktop>
            <div
              style={{ fontSize: "2.4em", height:"50px" }}
              className="my-2 vote-link text-center"
            >
              http:localhost:3000/3jhjgdhsvdb
            </div>
          </Desktop>
        </MDBCol>
      </MDBRow>
      <MDBRow center className="ml-3 my-4">
        <MDBCol className="justify-content-center">
          <h3 className=" title text-center">People Voted</h3>
        </MDBCol>
      </MDBRow>

      <MDBRow center className="ml-3 my-4">
        <MDBCol className="justify-content-center">
          <h1 className="  text-center">5</h1>
        </MDBCol>
      </MDBRow>
    </React.Fragment>
  );
};

const CandidateResult = () => {
  return (
    <MDBRow className=" my-2 overflow-auto">
      <MDBCol size="11" sm="11" className="">
        <div className="candidate-box">
          <div className="candidate-name-box">
            <span className="candidate-name">Girma</span>
            <span className="candidate-result">66%</span>
          </div>
          <MDBProgress
            className="my-2 progress-bg"
            material
            value={66}
            animated
            color="success"
          />
        </div>
      </MDBCol>
      <MDBCol size="1" sm="1" className="voter-count">
        <div> 3</div>
      </MDBCol>
    </MDBRow>
  );
};

export default AppResult;
