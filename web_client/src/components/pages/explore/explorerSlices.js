import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

export const initialState = {
  loading: true,
  error: false,
  isBlock: true,
  block: {
    index: null,
    hash: null,
    nonce: null,
    previousBlockHash: null,
    timestamp: null,
    transactions: [],
  },
  candidates: [],
};

export const fetchBlocks = createAsyncThunk(
  "blocks/fetchBlocks",
  async (search, thunkAPI) => {
    const { search_by, search_key } = search;
    console.log("serach:" + search_by, "searchKey:" + search_key);
    console.log("help");

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/" + search_by + "/" + search_key,
        {
          method: "GET",
        }
      );

      const data = await response.json();
      console.log(data);

      if (search_by === "vote") thunkAPI.dispatch(getCandidates(data));
      else thunkAPI.dispatch(getBlocks(data));
    } catch (error) {
      thunkAPI.dispatch(setError());
    }
  }
);

const blocksSlice = createSlice({
  name: "blocks",
  initialState,
  reducers: {
    getBlocks: (state, { payload }) => {
      state.loading = false;
      state.block = payload.block;
      state.isBlock = true;
      state.error = false;
    },
    getCandidates: (state, { payload, type }) => {
      state.loading = false;
      state.candidates = payload.candidates;
      state.isBlock = false;
      state.error = false;
    },
    setError: (state) => {
      state.error = true;
      state.loading = false;
    },
  },
});

export const { getBlocks, getCandidates, setError } = blocksSlice.actions;
export default blocksSlice.reducer;
