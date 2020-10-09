import React from 'react';
import { Route, Switch } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import ProfilePage from './pages/ProfilePage';
import TablesPage from './pages/TablesPage';
import NotFoundPage from './pages/NotFoundPage';
import AppResult from './pages/result/AppResult';
import HomePage from './pages/Homepage';
import BlockExplorer from './pages/explore/BlockExplorer';

class Routes extends React.Component {
  render() {
    return (
      <Switch>
        <Route path='/' exact component={DashboardPage} />
        <Route path='/dashboard' component={DashboardPage} />
        <Route path='/profile' component={ProfilePage} />
        <Route path='/home' component={HomePage} />
        <Route path='/explore' component={BlockExplorer} />
        <Route path='/result' component={AppResult} />
        <Route path='/tables' component={TablesPage} />
        <Route path='/404' component={NotFoundPage} />
      </Switch>
    );
  }
}

export default Routes;
