import React from "react";
import { MDBContainer, MDBIcon, MDBRow, MDBCol, MDBBtn } from "mdbreact";
import votingImage from "../../assets/voting_image.png";
import "./pages.css";
import BlockExplorer from "./explore/BlockExplorer";

const HomePage = () => {
  return (
    <React.Fragment>
      <MDBContainer className="my-5">
          <AppIntro/>
          <FeaturesPage/>
      </MDBContainer>
    </React.Fragment>
  );
};

const AppIntro = () => {
  return (
    <MDBRow>
      <MDBCol className="my-5">
        <div className="intro-title">
          ASTU Voting is a Secure Online Voting System
        </div>
        <div className="intro-descr my-5">
          Optimize your election with a blockchain-based online voting tool. It
          is easy to set up and use and no specific training or IT literacy is
          needed.
        </div>
        <MDBRow className="my-5 pt-5">
          <MDBCol>
            <MDBBtn rounded>Create Vote</MDBBtn>
          </MDBCol>
          <MDBCol>
            <MDBBtn outline> Getting Started</MDBBtn>
          </MDBCol>
        </MDBRow>
      </MDBCol>
      <MDBCol className="my-5">
        <img src={votingImage}></img>
      </MDBCol>
    </MDBRow>
  );
};


const FeaturesPage = () => {
  return (
    <section className="my-5">
      <h2 className="h1-responsive font-weight-bold text-center my-5">
        Why is it so great?
      </h2>
      <p className="lead grey-text w-responsive text-center mx-auto mb-5">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
        eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
        ad minim veniam.
      </p>

      <MDBRow>
        <MDBCol md="4" className="md-0 mb-5">
          <MDBRow>
            <MDBCol lg="2" md="3" size="2">
              <MDBIcon icon="bullhorn" size="2x" className="blue-text" />
            </MDBCol>
            <MDBCol lg="10" md="9" size="10">
              <h4 className="font-weight-bold">Marketing</h4>
              <p className="grey-text">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                do eiusmod tempor incididunt ut labore et dolore magna
                aliqua. Ut enim ad minim veniam.
              </p>
              <MDBBtn color="primary" size="sm">
                Learn more
              </MDBBtn>
            </MDBCol>
          </MDBRow>
        </MDBCol>
        <MDBCol md="4" className="md-0 mb-5">
          <MDBRow>
            <MDBCol lg="2" md="3" size="2">
              <MDBIcon icon="cogs" size="2x" className="pink-text" />
            </MDBCol>
            <MDBCol lg="10" md="9" size="10">
              <h4 className="font-weight-bold">Customization</h4>
              <p className="grey-text">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                do eiusmod tempor incididunt ut labore et dolore magna
                aliqua. Ut enim ad minim veniam.
              </p>
              <MDBBtn color="pink" size="sm">
                Learn more
              </MDBBtn>
            </MDBCol>
          </MDBRow>
        </MDBCol>
        <MDBCol md="4" className="md-0 mb-5">
          <MDBRow>
            <MDBCol lg="2" md="3" size="2">
              <MDBIcon icon="tachometer-alt" size="2x" className="purple-text" />
            </MDBCol>
            <MDBCol lg="10" md="9" size="10">
              <h4 className="font-weight-bold">Support</h4>
              <p className="grey-text">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                do eiusmod tempor incididunt ut labore et dolore magna
                aliqua. Ut enim ad minim veniam.
              </p>
              <MDBBtn color="purple" size="sm">
                Learn more
              </MDBBtn>
            </MDBCol>
          </MDBRow>
        </MDBCol>
      </MDBRow>
    </section>
  );
}

export default HomePage;
