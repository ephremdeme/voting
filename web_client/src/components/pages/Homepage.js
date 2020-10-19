import React from "react";
import { MDBContainer, MDBIcon, MDBRow, MDBCol, MDBBtn } from "mdbreact";
import votingImage from "../../assets/voting_image.png";
import "./pages.css";
import BlockExplorer from "./explore/BlockExplorer";

const HomePage = () => {
  return (
    <React.Fragment>
      <MDBContainer className="my-5">
        <AppIntro />
        <FeaturesPage />
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
      <h2 className=" h1-responsive font-weight-bold text-center my-5">
        Why is it so great?
      </h2>

      <MDBRow className="mt-5 py-5">
        <MDBCol md="4" className="md-0 mt-2 mb-5 vl-grey">
          <h4 className="font-weight-bold">Immutable and Anonymous</h4>
          <p className="feature-text my-3">
            Polys is based on blockchain technology, which makes voting 100%
            secure and immutable. Voter anonymity is guaranteed by transparent
            crypto algorithms.
          </p>
        </MDBCol>
        <MDBCol md="4" className="md-0 mb-5 vl-grey">
          <h4 className="font-weight-bold">Easy to organize, easy to vote</h4>
          <p className="feature-text my-3">
            With Polys, creating a vote is intuitive, easy and fast. No coding
            knowledge is required. Voting can be conducted on the go on a
            smartphone or tablet.
          </p>
        </MDBCol>
        <MDBCol md="4" className="md-0 mb-5">
          <h4 className="font-weight-bold">Transparent and auditable</h4>
          <p className="feature-text my-3">
            One of the main characteristics of blockchain technology is its
            transparency. The crypto algorithms that we use on top of it are
            merely mathematics.
          </p>
        </MDBCol>
      </MDBRow>
    </section>
  );
};

export default HomePage;
