import React, { useEffect } from "react";
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
import { fetchResult } from "./voteSlices";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { useState } from "react";

const AppResult = () => {
  const dispatch = useDispatch();
  const { loading, name, link, total, result } = useSelector(
    (state) => state.votes
  );
  const { vote_hash } = useParams();

  useEffect(() => {
    dispatch(fetchResult(vote_hash));
  }, [vote_hash, total]);

  console.log(result);

  return (
    <MDBContainer fluid className="py-2">
      <div className="my-3">
        <h1 className="title text-center mb-3">{name}</h1>
        <MobileOrTablet>
          <h3 className=" title text-center">Results</h3>
          {result.map((res, index) => (
            <CandidateResult total={total} candidate={res} key={index} />
          ))}

          <VoteInfo link={link} count={total} />
        </MobileOrTablet>

        <Desktop>
          <MDBCardBody className="mx-5 px-5">
            <MDBRow className="mx-5 px-5">
              <MDBCol className="vl" md="7">
                <MDBRow className=" my-4">
                  <MDBCol>
                    <h3 className=" title" style={{ fontStyle: "italic" }}>
                      Results
                    </h3>
                  </MDBCol>
                </MDBRow>
                {result.map((res, index) => (
                  <CandidateResult total={total} candidate={res} key={index} />
                ))}
              </MDBCol>

              <MDBCol md="5">
                <VoteInfo link={link} count={total} />
              </MDBCol>
            </MDBRow>
          </MDBCardBody>
        </Desktop>
      </div>
    </MDBContainer>
  );
};

const VoteInfo = ({ link, count }) => {
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
            <div className=" vote-link text-center">{link}</div>
          </MobileOrTablet>

          <Desktop>
            <div className=" col-6 vote-link text-center">{link}</div>
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
          <h1 className="  text-center">{count}</h1>
        </MDBCol>
      </MDBRow>
    </React.Fragment>
  );
};

export const  CandidateResult = ({ candidate, total }) => {
  const [percent, setPercent] = useState(parseInt(candidate[1] * 100/total));
  useEffect(() => {
    setPercent(parseInt(candidate[1] *100 / total));
  }, [candidate, total]);
  
  return (
    <MDBRow className=" my-2 overflow-auto">
      <MDBCol size="11" sm="11" className="">
        <div className="candidate-box">
          <div className="candidate-name-box">
            <span className="candidate-name">{candidate[0]}</span>
            <span className="candidate-result">{`${percent}%`}</span>
          </div>
          <MDBProgress
            className="my-2 progress-bg"
            material
            value={percent}
            animated
            color="success"
          />
        </div>
      </MDBCol>
      <MDBCol size="1" sm="1" className="voter-count">
        <div> {candidate[1]}</div>
      </MDBCol>
    </MDBRow>
  );
};

export default AppResult;
