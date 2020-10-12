import React from "react";
import { Route, Switch } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import ProfilePage from "./pages/ProfilePage";
import TablesPage from "./pages/TablesPage";
import NotFoundPage from "./pages/NotFoundPage";
import HomePage from "./pages/Homepage";
import BlockExplorer from "./pages/explore/BlockExplorer";
import SignUpPage from "./auth/SignUp";
import LogInPage from "./auth/Login";
import CreateVotePage from "./pages/vote/CreateVote";
import AppResult from "./pages/vote/AppResult";
import CastVotePage from "./pages/vote/CastVotePage";

class Routes extends React.Component {
  render() {
    return (
      <Switch>
         
        <Route path="/admin" component={DashboardPage} />
        <Route path="/profile" component={ProfilePage} />
        <Route path="/" exact component={HomePage} />
        <Route path="/explore" component={BlockExplorer} />
        <Route path="/result" exact component={AppResult} />
        <Route path="/vote/:vote_hash/result" component={AppResult} />
        <Route path="/vote/create_vote" component={CreateVotePage} />
        <Route path="/vote/:vote_hash/cast_vote" component={CastVotePage} />
        <Route path="/signup" component={SignUpPage} />
        <Route path="/login" component={LogInPage} />
        <Route path="/tables" component={TablesPage} />
        <Route path="/404" component={NotFoundPage} />
      </Switch>
    );
  }
}

export default Routes;
