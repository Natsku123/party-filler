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

import ChannelForm from './components/ChannelForm';
import PartyForm from './components/party/PartyForm';
import Parties from './components/party/Parties';
import Party from './components/party/Party';
import Games from './components/games/Games';
import Player from './components/Player';
import NotifySnackbar, { useSnackbar } from './components/NotifySnackbar';

import { playerService } from './services/players';

const baseUrl = ((window.REACT_APP_API_HOSTNAME) ? window.REACT_APP_API_HOSTNAME : 'http://localhost:8800');

const getLoginUrl = () => {
  return `${baseUrl}/login`;
};

const getLogoutUrl = () => {
  return `${baseUrl}/logout`;
};

const useStyles = makeStyles(() => ({
  link: {
    padding: 5,
  },
  grow: {
    flex: '1 1 auto',
  },
}));

const App = () => {
  const [ user, setUser ] = useState(null);
  const classes = useStyles();
  const {
    handleSnackbarClose,
    showSnackbar,
    snackbarStatus,
  } = useSnackbar();


  useEffect(() => {
    playerService
      .getCurrent()
      .then(res => setUser(res));
  }, []);

  const showSuccess = (message) => {
    showSnackbar(message, 'success');
  };

  const showError = (message) => {
    showSnackbar(message, 'error');
  };


  return (
    <Container>
      <Router basename="/#">
        <AppBar position='static'>
          <Toolbar>
            <IconButton edge="start" color="inherit" aria-label="menu"/>
            <Button color='inherit' component={Link} to="/" className={classes.link}>Home</Button>
            <Button color='inherit' component={Link} to="/channels/create" className={classes.link}>New Channel</Button>
            <Button color='inherit' component={Link} to="/parties/create" className={classes.link}>New Party</Button>
            <Button color='inherit' component={Link} to="/parties" className={classes.link}>Parties</Button>
            { user ?
              <div>
                <Button color='inherit' component={Link} to={"/games"} className={classes.link}>Games</Button>
                <Button color='inherit' component={Link} to={`/players/${user.id}`} className={classes.link}>{user.name}</Button>
                <Button color='inherit' component='a' href={ getLogoutUrl() } className={classes.link}>Logout</Button>
              </div> :
              <Button color='inherit' component='a' href={ getLoginUrl() } className={classes.link}>Login</Button>
            }
          </Toolbar>
        </AppBar>

        <Switch>
          <Route path="/channels/create">
            <ChannelForm onError={showError} onSuccess={showSuccess} />
          </Route>
          <Route path="/parties/create">
            <PartyForm onError={showError} onSuccess={showSuccess}/>
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

      </Router>

      <NotifySnackbar handleSnackbarClose={handleSnackbarClose} {...snackbarStatus} />
    </Container>
  );
};

export default App;
