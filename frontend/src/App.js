import React, { useState, useEffect } from 'react'
import {
  BrowserRouter as Router,
  Switch, Route, Link
} from 'react-router-dom'
import {
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Button, Snackbar,
} from '@material-ui/core'

import ChannelForm from './components/ChannelForm'
import PartyForm from './components/party/PartyForm'
import Parties from './components/Parties'
import Party from './components/party/Party'
import Player from './components/Player'

import { playerService } from './services/players'
import MuiAlert from "@material-ui/lab/Alert";

const baseUrl = ((window.REACT_APP_API_HOSTNAME) ? window.REACT_APP_API_HOSTNAME : 'http://localhost:8800');

const getLoginUrl = () => {

  /*
  const params = [
    'client_id=718047907617439804',
    `redirect_uir=${redirectUrl}/authorize`,
    'response_type=code',
    'scope=identify%20guilds'
  ].join('&')

  return `https://discord.com/api/oauth2/authorize?${params}`*/
  return `${baseUrl}/login`
}

const getLogoutUrl = () => {
  return `${baseUrl}/logout`
}

const App = () => {
  const [ user, setUser ] = useState(null)

  useEffect(() => {
    playerService
      .getCurrent()
      .then(res => setUser(res))
  }, [])

  const padding = {
    padding: 5
  }

  // Error handling
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarStatus, setSnackbarStatus] = useState("error");


  const Alert = (props) => {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
  }

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarOpen(false);
  };

  const showError = (message) => {
    setSnackbarMessage(message);
    setSnackbarStatus("error");
    setSnackbarOpen(true);
  }

  const showSuccess = (message) => {
    setSnackbarMessage(message);
    setSnackbarStatus("success");
    setSnackbarOpen(true);
  }

  return (
    <Container>
      <Router basename="/#">
        <AppBar position='static'>
          <Toolbar>
            <IconButton edge="start" color="inherit" aria-label="menu"/>
            <Button color='inherit' component={Link} to="/" style={padding}>Home</Button>
            <Button color='inherit' component={Link} to="/channels/create" style={padding}>New Channel</Button>
            <Button color='inherit' component={Link} to="/parties/create" style={padding}>New Party</Button>
            <Button color='inherit' component={Link} to="/parties" style={padding}>Parties</Button>
            { user ?
                <div>
                  <Button color='inherit' component={Link} to={`/players/${user.id}`} style={padding}>{user.name}</Button>
                  <Button color='inherit' component='a' href={ getLogoutUrl() } style={padding}>Logout</Button>
                </div> :
                <Button color='inherit' component='a' href={ getLoginUrl() } style={padding}>Login</Button>
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
          <Route path="/">
            <h1>Home Page</h1>
          </Route>
        </Switch>

      </Router>
      <Snackbar
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'center',
          }}
          open={snackbarOpen}
          autoHideDuration={6000}
          onClose={handleSnackbarClose}
      ><Alert severity={snackbarStatus}>{snackbarMessage}</Alert>
      </Snackbar>
    </Container>
  )
}

export default App
