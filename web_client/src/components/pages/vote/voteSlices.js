import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { saveAs } from "file-saver";
import { tokenConfig } from "../../../helper";

export const initialState = {
  error: null,
  loading: false,
  name: null,
  address: null,
  message: null,
  link: null,
  candidates: [],
  votes: [],
  result: [],
  total: null,
};

const voteSlices = createSlice({
  name: "votes",
  initialState,
  reducers: {
    createVote: (state, { payload }) => {
      state.name = payload.name;
      state.address = payload.address;
      state.loading = false;
    },
    castVote: (state, { payload }) => {
      state.message = payload.message;
      state.loading = false;
    },
    getVotes: (state, { payload }) => {
      state.votes = payload.votes;
      state.loading = false;
    },
    getResult: (state, { payload }) => {
      state.total = payload.total;
      state.result = payload.result;
      state.name = payload.name;
      state.link = payload.link;
      state.loading = false;
    },
    getCandidates: (state, { payload }) => {
      state.loading = false;
      state.candidates = payload.candidates;
    },
    setLoading: (state) => {
      state.loading = true;
    },
    setError: (state, { payload }) => {
      state.error = payload.msg;
      state.loading = false;
    },
  },
});

export const {
  createVote,
  getResult,
  getCandidates,
  setError,
  castVote,
  setLoading,
  getVotes,
} = voteSlices.actions;

export default voteSlices.reducer;

export const postVote = createAsyncThunk(
  "votes/postVote",
  async (form, thunkAPI) => {
    thunkAPI.dispatch(setLoading);
    try {
      const response = await fetch("http://127.0.0.1:5000/create_vote", {
        method: "POST",

        headers: tokenConfig().headers,
        body: JSON.stringify(form),
      });

      const data = await response.json();
      if (data.msg) thunkAPI.dispatch(setError(data));
      thunkAPI.dispatch(createVote(data));
    } catch (error) {
      thunkAPI.dispatch(setError(error));
    }
  }
);
export const castVotes = createAsyncThunk(
  "votes/castVotes",
  async (form, thunkAPI) => {
    thunkAPI.dispatch(setLoading);
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/vote/" + form.address + "/cast",
        {
          method: "POST",
          headers: tokenConfig().headers,
          body: JSON.stringify(form),
        }
      );

      const data = await response.json();
      if (data.msg) thunkAPI.dispatch(setError(data));
      thunkAPI.dispatch(castVote(data));
    } catch (error) {
      thunkAPI.dispatch(setError(error));
    }
  }
);

export const fetchResult = createAsyncThunk(
  "votes/fetchResult",
  async (address, thunkAPI) => {
    const { dispatch } = thunkAPI;
    dispatch(setLoading());
    try {
      const response = await fetch("http://127.0.0.1:5000/result/" + address, {
        method: "GET",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
        },
      });

      const data = await response.json();
      data["link"] = "http://127.0.0.1:5000/vote/" + address + "/cast";
      if (data.msg) dispatch(setError(data));
      dispatch(getResult(data));
    } catch (error) {
      setError(error);
    }
  }
);

export const fetchVotes = createAsyncThunk(
  "votes/fetchVotes",
  async (address, thunkAPI) => {
    const {dispatch} = thunkAPI
    const response = await fetch("http://127.0.0.1:5000/votes", {
      method: "GET",
      headers: tokenConfig().headers,
    });

    const data = await response.json();

    if (data.msg) dispatch(setError(data));
    dispatch(getVotes(data));
  }
);

export const fetchCandidates = createAsyncThunk(
  "votes/fetchCandidates",
  async (vote_hash, thunkAPI) => {
    const { dispatch } = thunkAPI;
    dispatch(setLoading());
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/vote/" + vote_hash + "/candidates",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json;charset=utf-8",
          },
        }
      );

      const data = await response.json();
      if (data.msg) dispatch(setError(data));
      dispatch(getCandidates(data));
    } catch (error) {
      setError(error);
    }
  }
);
// export const getFile = createAsyncThunk(
//   "votes/getFiles",
//   async (vote_hash, thunkAPI) => {
//     const { dispatch } = thunkAPI;
//     dispatch(setLoading());
//     try {
//       const response = await fetch("http://127.0.0.1:5000/file/" + vote_hash, {
//         method: "GET",
//         headers: tokenConfig().headers,
//       });
//       const data = await response.blob();

//       saveAs(data, "voter_list.xlsx");
//       // if (data.msg) dispatch(setError(data));
//       // dispatch(getCandidates(data));
//     } catch (error) {
//       setError(error);
//     }
//   }
// );
export const getFile = createAsyncThunk(
  "votes/getFiles",
  async (vote_hash, thunkAPI) => {
    const { dispatch } = thunkAPI;
    dispatch(setLoading());
    try {
      const response = await fetch("http://127.0.0.1:5000/file/" + vote_hash, {
        method: "GET",
        headers: tokenConfig().headers,
      });
      const data = await response.blob();

      saveAs(data, "voter_list.xlsx");
      // if (data.msg) dispatch(setError(data));
      // dispatch(getCandidates(data));
    } catch (error) {
      setError(error);
    }
  }
);
