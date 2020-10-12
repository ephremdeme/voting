import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { tokenConfig } from "../../helper";

export const initialState = {
  loading: false,
  error: null,
  isAuthenticated: false,
  token: localStorage.getItem("token") || null,
  user: {
    name: null,
    email: null,
    id: null,
  },
};

const authSlice = createSlice({
  name: "auths",
  initialState,
  reducers: {
    loginUser: (state, { payload }) => {
      state.error = null;
      state.loading = false;
      state.token = payload.token;
      state.user = payload.user;
      state.isAuthenticated = true;
      localStorage.setItem("token", payload.token);
    },
    getUser: (state, { payload }) => {
      state.user = payload.user;
      state.isAuthenticated = true;
    },
    signUp: (state, { payload }) => {
      state.error = null;
      state.loading = false;
      state.token = payload.token;
      state.isAuthenticated = true;
      state.user = payload.user;
      localStorage.setItem("token", payload.token);
    },
    setLoading: (state) => {
      state.loading = true;
    },
    setError: (state, { payload }) => {
      state.error = payload.msg;
      state.loading = false;
      state.isAuthenticated = false;
      localStorage.removeItem("token");
    },
  },
});

export const signInUser = createAsyncThunk(
  "auths/fetchUser",
  async (form, thunkAPI) => {
    thunkAPI.dispatch(setLoading());
    const { email, password } = form;
    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      const data = await response.json();
      console.log(data);
      if (data.msg) thunkAPI.dispatch(setError(data));
      thunkAPI.dispatch(loginUser(data));
    } catch (error) {
      thunkAPI.dispatch(setError(error));
    }
  }
);
export const signUpUser = createAsyncThunk(
  "auths/signUpUser",
  async (form, thunkAPI) => {
    thunkAPI.dispatch(setLoading());
    const { email, password, name } = form;
    try {
      const response = await fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
        },
        body: JSON.stringify({
          name: name,
          email: email,
          password: password,
        }),
      });

      const data = await response.json();
      console.log(data);
      if (data.msg) thunkAPI.dispatch(setError(data));
      thunkAPI.dispatch(signUp(data));
    } catch (error) {
      thunkAPI.dispatch(setError(error));
    }
  }
);

export const fetchUsers = createAsyncThunk(
  "auths/fetchUsers",
  async (address, thunkAPI) => {
    const { dispatch } = thunkAPI;
    dispatch(setLoading());
    const response = await fetch("http://127.0.0.1:5000/get_user", {
      method: "GET",
      headers: tokenConfig().headers,
    });

    const data = await response.json();
    if (data.msg) dispatch(setError(data));
    dispatch(getUser(data));
  }
);

export const {
  signUp,
  getUser,
  loginUser,
  setError,
  setLoading,
} = authSlice.actions;
export default authSlice.reducer;
