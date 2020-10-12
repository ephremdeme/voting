import { configureStore } from "@reduxjs/toolkit";
import blockReducer from "./components/pages/explore/explorerSlices";
import authReducer from "./components/auth/authSlices";
import voteSlices from "./components/pages/vote/voteSlices";

console.log(authReducer);

const store = configureStore({
  reducer: {
    blocks: blockReducer,
    auths: authReducer,
    votes: voteSlices,
  },
});

export default store;
