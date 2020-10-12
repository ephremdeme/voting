import React, { useState, useEffect } from "react";
import { MDBContainer, MDBBtn, MDBCol } from "mdbreact";
import "../pages.css";
import { useDispatch, useSelector } from "react-redux";
import { fetchBlocks } from "./explorerSlices";

const BlockExplorer = () => {
  const dispach = useDispatch();
  const { isBlock, error, block, candidates } = useSelector(
    (state) => state.blocks
  );

  const [search, setSearch] = useState({
    search_by: "block",
    search_key: "",
  });

  const [transactions, setTransactions] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSearch({
      ...search,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(search);
    dispach(fetchBlocks(search));
  };

  return (
    <section className="mt-5">
      <MDBContainer>
        <div className="row">
          <div className=" text-center col-12 my-3">
            <h1 className="page-title intro-title">Block Explorer</h1>
          </div>
        </div>
        <div className="row ">
          <div className="col-12 offset-md-2  my-3">
            <form onSubmit={handleSubmit}>
              <div className="form-group col-md-7 col-sm-7 my-4">
                <input
                  type="text"
                  onChange={handleChange}
                  id="key"
                  name="search_key"
                  placeholder="Block Index or Txs ID or Candidate ID"
                  className="form-control"
                />
              </div>
              <div className="form-group col-md-7 col-sm-7">
                <select
                  name="search_by"
                  onChange={handleChange}
                  id="searchBy"
                  className="form-control"
                >
                  <option value="block">Block Index</option>
                  <option value="transaction">Transaction ID</option>
                  <option value="vote">Candidate</option>
                </select>
              </div>
              <MDBBtn className="ml-5" type="submit" rounded>
                Search
              </MDBBtn>
            </form>
            {error && <p className="no-data-text">No data found for search.</p>}
          </div>
        </div>

        {isBlock && <ShowBlock block={block} />}
        {isBlock && <ShowTxs transactions={block.transactions} />}
        {!isBlock && <ShowTxs transactions={candidates} />}
      </MDBContainer>
    </section>
  );
};

const BlockDisplay = ({ block, candidates }) => {
  return (
    <React.Fragment>
      <div className="row">
        <div className="col">
          <ShowBlock block={block} />
        </div>
      </div>
      <div className="row mb-5 pb-5">
        <MDBCol>
          <ShowTxs transactions={candidates || block.transactions} />
        </MDBCol>
      </div>
    </React.Fragment>
  );
};

const ShowTxs = ({ transactions }) => {
  return (
    <React.Fragment>
      <div className="row mb-5 pb-5">
        <MDBCol>
          <h3 className="table-title intro-title" >
            Vote
          </h3>
          <table className="table table-borderless" >
            <thead className="thead-dark">
              <tr>
                <th scope="col">#</th> <th scope="col">Tx ID</th>
                <th scope="col">VOTER</th> <th scope="col">CANDIDATE</th>
              </tr>
            </thead>
            <tbody className="overflow-auto">
              {transactions.map((tx, ind) => (
                <tr>
                  <td>{ind + 1}</td>
                  <td>{tx.id}</td>
                  <td>{tx.from_address}</td>
                  <td>{tx.to_address}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </MDBCol>
      </div>
    </React.Fragment>
  );
};

const ShowBlock = ({ block }) => {
  return (
    <React.Fragment>
      <div className="row">
        <div className="col">
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
        </div>
      </div>
    </React.Fragment>
  );
};
export default BlockExplorer;
