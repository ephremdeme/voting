import React, { useState } from "react";
import { MDBContainer, MDBBtn, MDBCol } from "mdbreact";
import "../pages.css";

const BlockExplorer = () => {
  const [isFound, setIsFound] = useState(false);

  return (
    <section className="mt-5 pt-4">
      <MDBContainer>
        <div className="row">
          <div className=" text-center col-12 my-3">
            <h1 className="page-title intro-title">Block Explorer</h1>
          </div>
        </div>
        <div className="row ">
          <div className="col-12 offset-md-4  my-3">
            <form>
              <div className="form-group col-md-7 col-sm-7 my-4">
                <input
                  type="text"
                  id="key"
                  placeholder="Block Index or Txs ID or Candidate ID"
                  className="form-control"
                />
              </div>
              <div className="form-group col-md-7 col-sm-7">
                <select id="searchBy" className="form-control">
                  <option value="block">Block Index</option>
                  <option value="transaction">Transaction ID</option>
                  <option value="vote">Candidate</option>
                </select>
              </div>
              <MDBBtn className="ml-5" type="submit" rounded>
                Search
              </MDBBtn>
            </form>
            {isFound && (
              <p className="no-data-text">No data found for search.</p>
            )}
          </div>
        </div>

        <BlockDisplay />
      </MDBContainer>
    </section>
  );
};

const BlockDisplay = () => {
  return (
    <div className="row">
      <div className="col">
        <ShowBlock block={"help"} />
      </div>
      <MDBCol>
        <ShowTxs transaction={"hjbh"} />
      </MDBCol>
    </div>
  );
};

const ShowTxs = ({ transaction }) => {
  return (
    <React.Fragment>
      <h3 className="table-title intro-title" ng-if="transaction">
        Vote
      </h3>
      <table className="table table-borderless" ng-if="transaction">
        <thead class="thead-dark">
          <tr>
            <th scope="col">#</th> <th scope="col">ID</th>{" "}
            <th scope="col">VOTER</th> <th scope="col">CANDIDATE</th>{" "}
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>{transaction}</td>
            <td>Recipient</td>
            <td>{transaction}</td>
          </tr>
        </tbody>
      </table>
    </React.Fragment>
  );
};

const ShowBlock = ({ block }) => {
  return (
    <React.Fragment>
      <h3 className="table-title intro-title" ng-if="block">
        Block
      </h3>
      <table className="table " ng-if="block">
        <tbody>
          <tr>
            <td className="font-weight-normal">Block Hash</td>
            <td>{block.hash}</td>
          </tr>
          <tr>
            <td className="font-weight-normal">Index</td>
            <td>{block.index}</td>
          </tr>
          <tr>
            <td className="font-weight-normal">Time Stamp</td>
            <td>{block.timestamp}</td>
          </tr>
          <tr>
            <td className="font-weight-normal">Nonce</td>
            <td>{block.nonce}</td>
          </tr>
          <tr>
            <td className="font-weight-normal">Previous Hash</td>
            <td>{block.previousBlockHash}</td>
          </tr>
        </tbody>
      </table>
    </React.Fragment>
  );
};
export default BlockExplorer;
