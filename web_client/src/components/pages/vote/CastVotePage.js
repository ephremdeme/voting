import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBBtn,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBStepper,
  MDBStep,
  MDBLink,
  MDBInputGroup,
  MDBFormInline,
  MDBAlert,
} from "mdbreact";
import { fetchCandidates, getFile, castVotes } from "./voteSlices";
import { useParams } from "react-router-dom";

const CastVotePage = () => {
  const dispatch = useDispatch();
  const { vote_hash } = useParams();

  const [values, setValues] = useState({
    formActivePanel1: 1,
    formActivePanel1Changed: false,
  });

  const [voteData, setVoteData] = useState({
    pin: null,
    address: vote_hash,
    candidate_addr: null,
  });

  const [radio, setRadio] = useState(1);

  const onChecked = (rn) => () => {
    setRadio(rn);
    console.log(radio);
  };

  const { loading, error, name, address, message, candidates } = useSelector(
    (state) => state.votes
  );

  useEffect(() => {
    dispatch(fetchCandidates(vote_hash));
  }, [vote_hash]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setVoteData({
      ...voteData,
      [name]: value,
    });
  };

  const handleSubmit = () => {
    dispatch(castVotes(voteData));
    console.log(voteData);
  };

  const swapFormActive = (a) => (param) => (e) => {
    setValues({
      ["formActivePanel" + a]: param,
      ["formActivePanel" + a + "Changed"]: true,
    });
  };

  const handleNextPrevClick = (a) => (param) => (e) => {
    setValues({
      ["formActivePanel" + a]: param,
      ["formActivePanel" + a + "Changed"]: true,
    });
  };

  const calculateAutofocus = (a) => {
    if (values["formActivePanel" + a + "Changed"]) {
      return true;
    }
  };

  const Flash = () => {
    return (
      <React.Fragment>
        {message && <Alert message={message} type="success" />}
        {error && <Alert message={error} type="warning" />}
      </React.Fragment>
    );
  };

  const Alert = ({ message, type }) => {
    return (
      <div
        className={`alert alert-${type} alert-dismissible fade show`}
        role="alert"
      >
        {message}
        <button
          type="button"
          className="close"
          data-dismiss="alert"
          aria-label="Close"
        >
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
    );
  };

  return (
    <MDBContainer className="my-5 py-5">
      <Flash />
      <MDBRow center>
        <MDBCol xl="6" lg="7" md="10">
          <MDBCard>
            <MDBCardBody>
              <div className="header my-3 unique-color-dark lighten-2">
                <MDBRow className="d-flex justify-content-center">
                  <h3 className="text-white font-weight-normal my-3 mx-5">
                    Cast Your Vote
                  </h3>
                </MDBRow>
              </div>
              <MDBStepper form>
                <MDBStep form>
                  <a href="#formstep1" onClick={swapFormActive(1)(1)}>
                    <MDBBtn
                      color={
                        values.formActivePanel1 === 1 ? "indigo" : "default"
                      }
                      circle
                    >
                      1
                    </MDBBtn>
                  </a>
                  <p>Insert Pin </p>
                </MDBStep>
                <MDBStep form>
                  <a href="#formstep2" onClick={swapFormActive(1)(2)}>
                    <MDBBtn
                      color={
                        values.formActivePanel1 === 2 ? "indigo" : "default"
                      }
                      circle
                    >
                      2
                    </MDBBtn>
                  </a>
                  <p>Vote</p>
                </MDBStep>
                <MDBStep form>
                  <a href="#formstep3" onClick={swapFormActive(1)(3)}>
                    <MDBBtn
                      color={
                        values.formActivePanel1 === 3 ? "indigo" : "default"
                      }
                      circle
                    >
                      3
                    </MDBBtn>
                  </a>
                  <p>Finish</p>
                </MDBStep>
              </MDBStepper>

              <div>
                <MDBRow>
                  {values.formActivePanel1 === 1 && (
                    <MDBCol md="12">
                      <h3 className="font-weight-bold pl-0 my-4">
                        <strong>Insert Your Pin</strong>
                      </h3>
                      <MDBInput
                        label="Your Pin"
                        name="pin"
                        onChange={handleChange}
                        className="mt-3"
                        autoFocus={calculateAutofocus(1)}
                      />
                      <MDBBtn
                        color="indigo"
                        rounded
                        className="float-right"
                        onClick={handleNextPrevClick(1)(2)}
                      >
                        next
                      </MDBBtn>
                    </MDBCol>
                  )}
                  {values.formActivePanel1 === 2 && (
                    <MDBCol md="12">
                      <h3 className="font-weight-bold pl-0 my-4">
                        <strong>Choose a Candidate</strong>
                      </h3>
                      <MDBFormInline className="my-3 justify-content-center">
                        {candidates.map((item, index) => (
                          <div className="mx-2" key={index}>
                            <MDBInput
                              id={`radio${index}`}
                              value={item[0]}
                              checked={radio === index ? true : false}
                              onClick={onChecked(index)}
                              getValue={(val) =>
                                setVoteData({
                                  ...voteData,
                                  candidate_addr: val,
                                })
                              }
                              type="radio"
                              label={item[1]}
                              className="mt-4"
                              autoFocus={calculateAutofocus(1)}
                            />
                          </div>
                        ))}
                      </MDBFormInline>
                      <MDBBtn
                        color="indigo"
                        rounded
                        className="float-left"
                        onClick={handleNextPrevClick(1)(1)}
                      >
                        previous
                      </MDBBtn>
                      <MDBBtn
                        color="indigo"
                        rounded
                        className="float-right"
                        onClick={handleNextPrevClick(1)(3)}
                      >
                        next
                      </MDBBtn>
                    </MDBCol>
                  )}
                  {values.formActivePanel1 === 3 && (
                    <MDBCol md="12">
                      <h3 className="font-weight-bold pl-0 my-4">
                        <strong>Thank You!</strong>
                      </h3>
                      <MDBBtn
                        color="indigo"
                        rounded
                        className="float-left"
                        onClick={handleNextPrevClick(1)(2)}
                        autoFocus={calculateAutofocus(1)}
                      >
                        previous
                      </MDBBtn>
                      <MDBBtn
                        color="default"
                        rounded
                        className="float-right"
                        onClick={handleSubmit}
                      >
                        submit
                      </MDBBtn>
                    </MDBCol>
                  )}
                </MDBRow>
              </div>
            </MDBCardBody>
          </MDBCard>
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
};

export default CastVotePage;

// const CastVotePage = () => {
//   const dispatch = useDispatch();
//   const { loading, error, name, address, candidates } = useSelector(
//     (state) => state.votes
//   );

//   const { vote_hash } = useParams();

//   const [values, setValues] = useState({
//     voter_count: null,
//     name: null,
//     organizer: null,
//   });

//   useEffect(() => {
//     dispatch(fetchCandidates(vote_hash));
//   }, [vote_hash]);

//   console.log(candidates);

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setValues({
//       ...values,
//       [name]: value,
//     });
//   };

//   const handleSubmit = () => {};

//   return (
//     <React.Fragment>
//       <MDBContainer className="my-5 py-5">
//         <MDBRow center>
//           <MDBCol md="6">
//             <MDBCard>
//               <div className="header pt-3 unique-color-dark lighten-2">
//                 <MDBRow className="d-flex justify-content-start">
//                   <h3 className="text-white font-weight-normal mt-3 mb-4 pb-1 mx-5">
//                     Cast Your Vote
//                   </h3>
//                 </MDBRow>
//               </div>
//               <MDBCardBody className="mx-4 mt-4">
//                 <MDBInput
//                   name="name"
//                   onChange={handleChange}
//                   label="Election Name"
//                   group
//                   type="text"
//                   validate
//                 />

//                 <MDBInput
//                   label="Organizer Name"
//                   group
//                   onChange={handleChange}
//                   name="organizer"
//                   type="text"
//                   validate
//                   containerClassNamclassName="mb-0"
//                 />

//                 <div className="text-center mb-4 mt-5">
//                   <MDBBtn
//                     rounded
//                     onClick={handleSubmit}
//                     color="unique-color-dark"
//                     type="button"
//                     className="btn-block text-white z-depth-2 unique-color-dark"
//                   >
//                     Cast Vote
//                   </MDBBtn>
//                 </div>

//                 {/* <SteperComp /> */}
//               </MDBCardBody>
//             </MDBCard>
//           </MDBCol>
//         </MDBRow>
//       </MDBContainer>
//     </React.Fragment>
//   );
// };
