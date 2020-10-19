import React from "react";
import { MDBRow, MDBContainer, MDBCol, MDBBtn, MDBLink } from "mdbreact";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { fetchVotes, fetchResult } from "./vote/voteSlices";
import { CandidateResult } from "./vote/AppResult";
import { Link } from "react-router-dom";
import { useState } from "react";

const DashboardPage = () => {
  const dispatch = useDispatch();
  const [address, setAddress] = useState(null);
  const { votes, loading, result, total } = useSelector((state) => state.votes);

  useEffect(() => {
    dispatch(fetchVotes());
  }, [loading]);

  const handleClick = (hash) => {
    dispatch(fetchResult(hash));
    setAddress(hash);
  };
  return (
    <React.Fragment>
      <MDBContainer fluid className=" dashboard">
        <MDBRow className="dashboard">
          <MDBCol md="3" className="left px-2">
            <div className="my-3 ml-3">
              <Link
                to="/vote/create_vote"
                rounded
                outline
                className="mx-2 btn btn-outline-default btn-rounded"
              >
                Create Vote
              </Link>
            </div>
            <div>
              {votes.map((vote, index) => (
                <React.Fragment key={index}>
                  <MDBLink
                    onClick={() => handleClick(vote.hash)}
                    className="font-weight-normal"
                    active={true}
                    to={"#!"}
                  >
                    {vote.vote_name}
                  </MDBLink>
                  <hr className="my-2" />
                </React.Fragment>
              ))}
            </div>
          </MDBCol>
          <MDBCol md="9" className="right pl-5 pt-5">
            <MDBRow className=" my-4">
              <MDBCol className="text-center">
                <h3 className=" title" style={{ fontStyle: "italic" }}>
                  Results
                </h3>
              </MDBCol>
            </MDBRow>
            {result.map((res, index) => (
              <CandidateResult total={total} candidate={res} key={index} />
            ))}
            {address && (
              <MDBRow className="my-4 text-black">
                <MDBCol>
                  <MDBBtn
                    target="_blanc"
                    href={`/vote/${address}/result`}
                    outline
                  >
                    Public Display
                  </MDBBtn>
                </MDBCol>
                <MDBCol>
                  <MDBBtn
                    target="_blanc"
                    href={`/vote/${address}/cast_vote`}
                    outline
                  >
                    Public Vote
                  </MDBBtn>
                </MDBCol>
                <MDBCol className="text-center">
                  <h3 className="title">People Voted : {total}</h3>
                </MDBCol>
              </MDBRow>
            )}
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </React.Fragment>
  );
};

export default DashboardPage;
