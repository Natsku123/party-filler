import React, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Switch, Route, Link
} from 'react-router-dom';
import {
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Button,
  Grid,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

import PartyCreate from './components/party/PartyCreate';
import Parties from './components/party/Parties';
import Party from './components/party/Party';
import Games from './components/games/Games';
import Player from './components/Player';
import NotifySnackbar, { useSnackbar } from './components/NotifySnackbar';
import Layout from './components/Layout';


const useStyles = makeStyles(() => ({
  link: {
    padding: 5,
  },
  grow: {
    flex: '1 1 auto',
  },
}));

const App = () => {
  const classes = useStyles();
  const {
    handleSnackbarClose,
    showSnackbar,
    snackbarStatus,
  } = useSnackbar();


  const showSuccess = (message) => {
    showSnackbar(message, 'success');
  };

  const showError = (message) => {
    showSnackbar(message, 'error');
  };


  return (
    <>
      <Router basename="/#">
        <Layout>

          <Switch>
            <Route path="/parties/create">
              <PartyCreate onError={showError} onSuccess={showSuccess}/>
            </Route>
            <Route path="/parties/:id">
              <Party onError={showError} onSuccess={showSuccess}/>
            </Route>
            <Route path="/parties">
              <Parties onError={showError}/>
            </Route>
            <Route path="/players/:id">
              <Player onError={showError}/>
            </Route>
            <Route path="/games">
              <Games />
            </Route>
            <Route path="/">
              <h1>Home Page</h1>
            </Route>
          </Switch>

        </Layout>
      </Router>

      <NotifySnackbar handleSnackbarClose={handleSnackbarClose} {...snackbarStatus} />
    </>
  );
};

export default App;
