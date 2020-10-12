import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBBtn,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBLink,
  MDBInputGroup,
} from "mdbreact";
import { postVote, getFile } from "./voteSlices";

const CreateVotePage = () => {
  const dispatch = useDispatch();
  const { loading, error, name, address } = useSelector((state) => state.votes);

  const [values, setValues] = useState({
    voter_count: null,
    name: null,
    organizer: null,
    candidates: [],
  });

  const [candidate, setCandidate] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues({
      ...values,
      [name]: value,
    });
  };

  const clickHandler = (cand) => {
    setValues({
      ...values,
      candidates: values.candidates.filter((item) => item != cand),
    });
  };

  const handleCandidate = (e) => {
    setValues({
      ...values,
      candidates: [...values["candidates"], candidate],
    });
    setCandidate("");
  };

  if(address) dispatch(getFile(address))

  const handleSubmit = () => {
    dispatch(postVote(values));
  };

  return (
    <React.Fragment>
      <MDBContainer className="my-5 py-5">
        <MDBRow center>
          <MDBCol md="6">
            <MDBCard>
              <div className="header pt-3 unique-color-dark lighten-2">
                <MDBRow className="d-flex justify-content-start">
                  <h3 className="text-white font-weight-normal mt-3 mb-4 pb-1 mx-5">
                    Create a Vote
                  </h3>
                </MDBRow>
              </div>
              <MDBCardBody className="mx-4 mt-4">
                <MDBInput
                  name="name"
                  onChange={handleChange}
                  label="Election Name"
                  group
                  type="text"
                  validate
                />

                <MDBInput
                  label="Organizer Name"
                  group
                  onChange={handleChange}
                  name="organizer"
                  type="text"
                  validate
                  containerClass="mb-0"
                />

                <MDBInput
                  name="voter_count"
                  onChange={handleChange}
                  label="Number of Voters"
                  group
                  max="100"
                  type="number"
                  validate
                />

                <MDBInputGroup
                  material
                  containerClassName="mb-3 mt-0"
                  hint="Candidate Name"
                  name="candidate"
                  valueDefault={candidate}
                  value={candidate}
                  getValue={(e) => setCandidate(e)}
                  append={
                    <MDBBtn
                      type="button"
                      rounded
                      onClick={handleCandidate}
                      className="m-0 px-3 py-2 z-depth-2 text-white unique-color-dark"
                    >
                      Add
                    </MDBBtn>
                  }
                />
                <CandidateList
                  clickHandler={clickHandler}
                  candidates={values.candidates}
                />
                <div className="text-center mb-4 mt-5">
                  <MDBBtn
                    rounded
                    onClick={handleSubmit}
                    color="unique-color-dark"
                    type="button"
                    className="btn-block text-white z-depth-2 unique-color-dark"
                  >
                    Create Vote
                  </MDBBtn>
                </div>
              </MDBCardBody>
            </MDBCard>
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </React.Fragment>
  );
};

const CandidateList = ({ candidates, clickHandler }) => {
  return (
    <React.Fragment>
      <ul className="p-0">
        {candidates.map((cand, index) => (
          <li style={{ listStyle: "none" }} key={index}>
            {cand}
            <span
              onClick={() => clickHandler(cand)}
              className="float-right red-text"
            >
              X
            </span>
          </li>
        ))}
      </ul>
    </React.Fragment>
  );
};

export default CreateVotePage;
